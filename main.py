#!//usr/bin/python
# Hint: for nice stats top-100 you can call
# cat messages_from_chat |grep \| | cut -f 1 -d \| |sort|uniq -c|sort -nr | head -100|nl|sed -e 's/None/-/g'
import asyncio
from telethon import TelegramClient
from telethon.tl.types import PeerChannel, PeerUser
from telethon.tl.functions.messages import GetHistoryRequest
import argparse

parser = argparse.ArgumentParser(description='Simple telegram channel backup utility')
parser.add_argument("--api", default="w", help="api_id")
parser.add_argument("--hash", default="0", help="hash")
parser.add_argument("--channel", default="0", help="Channel ID")
parser.add_argument("--task", default="list", help="What to do? list of grab")
args = parser.parse_args()

api_id = 0
api_hash = ""
try:
    api_id = int(args.api)
except:
    print("Bad api_id")
    exit(1)

if args.hash == "0":
    print("Set api_hash")
    exit(1)

api_hash = args.hash

client = TelegramClient('teleclient_session', api_id, api_hash)
client.start()

async def get_channels():
    s = await client.get_dialogs()
    # print(s[0])
    for i in range(len(s)):
        try:
            print(s[i].entity.id, s[i].entity.title)
        except:
            print(s[i].entity.id, s[i].entity.first_name, s[i].entity.last_name, s[i].entity.username)


async def dump_messages():

    f=open('messages_from_chat', 'w')

    offset=0

    ch_ent = await client.get_entity(PeerChannel(1149668735))

    user_id = {}
    first_name = {}
    second_name = {}
    nickname = {}

    while True:
        posts = await client(GetHistoryRequest(
            peer=ch_ent,
            limit=80,
            offset_date=None,
            offset_id=offset,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0))


        for message in posts.messages:
            us_id = message.from_id
            if us_id not in user_id:
                user = await client.get_entity(PeerUser(us_id))
                user_id[us_id] = "1"
                first_name[us_id] = user.first_name
                second_name[us_id] = user.last_name
                nickname[us_id] = user.username

            print("%s %s %s | %s" % (first_name[us_id],second_name[us_id],nickname[us_id], message.message), file=f)
            print("%s %s %s | %s" % (first_name[us_id], second_name[us_id], nickname[us_id], message.message))
            offset=message.id

        f.flush()
        await asyncio.sleep(1)

    f.close()


loop = asyncio.get_event_loop()

if args.task == "list":
    loop.run_until_complete(asyncio.gather(get_channels()))

if args.task == "grab":
    if args.channel == "0":
        print("Set Channel ID")
        exit(0)
    loop.run_until_complete(asyncio.gather(dump_messages()))


tasks = Task.all_tasks()
for t in [t for t in tasks if not (t.done() or t.cancelled())]:
    loop.run_until_complete(t)    # give canceled tasks the last chance to run
