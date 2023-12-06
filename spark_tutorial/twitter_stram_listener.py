import socket
import tweepy
import json

# Twitter credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# Tweepy setup
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define the list of terms to listen to
LISTEN_TERMS = ['happy', 'money']

# TCP socket setup
TCP_IP = "localhost"
TCP_PORT = 9009

# Create a socket object
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print(f"Listening on port: {TCP_PORT}")

# Class for handling Twitter Stream
class TweetListener(tweepy.StreamListener):
    def on_status(self, status):
        global conn
        if conn:
            try:
                tweet_text = status.extended_tweet["full_text"]
            except AttributeError:
                tweet_text = status.text
            print(tweet_text)
            conn.send(tweet_text.encode('utf-8'))

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        return False

# Wait for a connection
conn, addr = s.accept()

# Setup stream listener
stream_listener = TweetListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# Start streaming
stream.filter(track=LISTEN_TERMS)
