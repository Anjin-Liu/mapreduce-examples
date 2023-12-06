import socket
import time
import random

# TCP socket setup
TCP_IP = 'localhost'
TCP_PORT = 9010
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print(f"Listening on port: {TCP_PORT}")
conn, addr = s.accept()

try:
    while True:
        # Generate a random number
        number = random.randint(1, 1000)
        print(f"Sending number: {number}")

        # Send the number over the socket
        conn.send(f"{number}\n".encode('utf-8'))

        # Wait for a second before sending the next number
        time.sleep(5)
except KeyboardInterrupt:
    print("Interrupted by the user")

conn.close()
