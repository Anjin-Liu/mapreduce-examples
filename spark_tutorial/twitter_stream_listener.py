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

# Wait for a connection
conn, addr = s.accept()

# Function to send data to socket
def send_to_socket(data):
    global conn
    if conn:
        try:
            tweet_text = json.loads(data)['data']['text']
            print(tweet_text)
            conn.send(tweet_text.encode('utf-8'))
        except:
            pass

# Stream class using the new Tweepy implementation
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        send_to_socket(json.dumps({'data': tweet}))

# Initialize and start the stream
stream = MyStream(bearer_token=api.auth.access_token)
for term in LISTEN_TERMS:
    stream.add_rules(tweepy.StreamRule(term))
stream.filter()
