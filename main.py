from twitchobserver import Observer
import time
import threading

# change these to be, well, you
#using 'bot_tester_bot' twitch account, password 'bot_tester_bo'.
CHANNEL_1 ='nbso98'
CHANNEL_2 = 'bot_tester_bot'
USER = 'nbso98'
AUTHKEY = 'oauth:89p2rs5jcrj7ko2q7px2w2lrc3om3y'

if (AUTHKEY=='UNSET'):
    raise NotImplementedError("this isn't going to work, you need to set your username and authkey")

# your code goes here!
def message(text, user):
    return "%s to you too, %s" % (text, user)

# we keep a list of message IDs we've seen before just in case we see them twice
seenBefore = set()

print("connecting")
observer = Observer(USER, AUTHKEY)


with observer:
    print("joining C 1")
    observer.join_channel(CHANNEL_1)
    print("running in C 1")
    print("joining C 2")
    observer.join_channel(CHANNEL_2)
    print("running in C 2")

    print("running")
    try:
        while True:
            e = observer.get_events()
            if(len(e)>0):
                print("got %i events" % len(e))

            for event in e:
                if (hasattr(event, "tags")):
                    if (event.tags.get("id")):
                        print("ID is %s %s " % (event.tags.get("id"), seenBefore))
                        if (event.tags.get("id") in seenBefore):
                            # duplicate message
                            continue
                        else:
                            seenBefore.add(event.tags.get("id"))
                print(event)
                if event.type == 'TWITCHCHATMESSAGE':
                    if CHANNEL_1 == event.channel:
                        new_chan = CHANNEL_2
                    else:
                        new_chan = CHANNEL_1
                    reply = message(event.message, new_chan)
                    if (reply):
                        observer.send_message(reply, new_chan)

            # never post too fast, even in response to messages that arrive. Twitch will block us.
            time.sleep(0.1)

    except KeyboardInterrupt:
        observer.leave_channel(CHANNEL_1)
        observer.leave_channel(CHANNEL_2)
