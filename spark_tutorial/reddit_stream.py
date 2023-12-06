import socket
import praw
import json

# Reddit credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
user_agent = 'YOUR_USER_AGENT'

# PRAW setup
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# TCP socket setup
TCP_IP = 'localhost'
TCP_PORT = 9010
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print(f"Listening on port: {TCP_PORT}")

conn, addr = s.accept()

# Stream Reddit submissions
subreddit = reddit.subreddit('all')
for submission in subreddit.stream.submissions():
    try:
        if 'happy' in submission.title.lower() or 'money' in submission.title.lower():
            data = {'title': submission.title, 'url': submission.url}
            
            # Print the received message
            print("Received a post:", json.dumps(data))

            # Send data to TCP socket
            conn.send(json.dumps(data).encode('utf-8'))
    except Exception as e:
        print(e)
