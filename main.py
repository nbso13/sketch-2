from twitchobserver import Observer
import time
import threading
import random
import eliza

therapist = eliza.eliza()

# change these to be, well, you
#using 'bot_tester_bot' twitch account, password 'bot_tester_bo'.
CHANNEL_1 ='nbso98'
CHANNEL_2 = 'neha_linga'
USER = 'b0neb0neb0neb0ne'
AUTHKEY = 'oauth:wpwvpj72lump8rmzgm180ob1k6d5rv'

if (AUTHKEY=='UNSET'):
    raise NotImplementedError("this isn't going to work, you need to set your username and authkey")

# your code goes here!
def message(reply, user):
    # figure out which channel we're dealing with
    if user == CHANNEL_1:
        ind = 1 #refering to chan2
    else:
        ind = 0 #ref chan1
    if not(chan_replies[ind]): #if empty list
        # eliza replies to you directly
        text = therapist.respond(reply)
        # defaultReplies[random.randint(0, len(defaultReplies)-1)]
    else:
        #otherwise parse last reply from other chan
        chan_rep = chan_replies[ind].pop()
        text = therapist.respond(chan_rep)
    return text

# we keep a list of message IDs we've seen before just in case we see them twice
seenBefore = set()

# save replies from each person: first list is chan 1, second is chan 2 
# and then congregates all responses in all_replies
chan_replies = list([list(), list()])
all_replies = set()

# if you get texted and the other person hasn't said anything, use this
defaultReplies = list(["Nah fuck YOU.", "Ikr?!", "The odds point to ~maybe~"])

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
                        chan_ind = 0 #came from first chan
                    else:
                        chan_ind = 1 #came from first chan
                    # add to appropriate list
                    chan_replies[chan_ind].append(event.message)
                    # add to master list
                    all_replies.append(event.message)
                    reply = message(event.message, event.channel)
                    if (reply):
                        all_replies.append(reply)
                        observer.send_message(reply, event.channel)

            # never post too fast, even in response to messages that arrive. Twitch will block us.
            time.sleep(0.1)

    except KeyboardInterrupt:
        observer.leave_channel(CHANNEL_1)
        observer.leave_channel(CHANNEL_2)
