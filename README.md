# sketch-2

> a twitch chatbot that mediates a conversation between two users.

Improvements to be made:
1. Instead of drawing from that random list of phrases in main.py when the other user has not put anything into the chat room, have the bot respond using Eliza code.
2. Build in sentiment analysis code and run it on the other user's phrases. (consider using TextBlob for sentiment analysis /noun swapping).

Note: I added in TextBlob parsing (needs to be made better). to run this, install textblob:
$ pip install -U textblob
$ python -m textblob.download_corpora
