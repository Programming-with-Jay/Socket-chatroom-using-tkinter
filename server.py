import socket
import time
import threading

PORT = 5000

SERVER = "YOUR IPV4"

ADDRESS = (SERVER, PORT)

FORMAT = "utf-8"

clients, names = [], []

server = socket.socket(socket.AF_INET,
					socket.SOCK_STREAM)
server.bind(ADDRESS)

def start():
	
	print("server is working on " + SERVER)
	
	# listening for connections
	server.listen()
	
	while True:
		
		# accept connections and returns
		# a new connection to the client
		# and the address bound to it
		conn, addr = server.accept()
		conn.send("NAME".encode(FORMAT))
		
	
		name = conn.recv(1024).decode(FORMAT)

		names.append(name)
		clients.append(conn)
		
		print(f"Name is :{name}")
		
		# broadcast message
		message_to_clients(f"{name} has joined the chat!".encode(FORMAT))
		
		conn.send('Connection successful!'.encode(FORMAT))
		
		# Start the handling thread
		thread = threading.Thread(target = message_from_client,
								args = (conn, addr))
		thread.start()
		
		print(f"active connections {threading.activeCount()-1}")

def message_from_client(conn, addr):
	
	print(f"new connection {addr}")
	connected = True
	
	while connected:
		# recieve message
		message = conn.recv(1024)
		
		# broadcast message
		message_to_clients(message)
	
	# close the connection
	conn.close()

# messages to the each clients
def message_to_clients(message):
	for client in clients:
		client.send(message)

# call the method to
# begin the communication
start()
