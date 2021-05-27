#imports
import socket
import time
import threading


# variables
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
clients, names = [], []


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # initializing the socket
server.bind(ADDRESS)    # Bonding the server with the ADDRESS.


def start():
    """
    <summary>
    this function starts the server and prints the essential informations.
    </summary>
    :return: None
    """
    print("server is working on " + SERVER)

    # listening for connections
    server.listen()

    while True:
        """ accept connections and returns 
        a new connection to the client and the 
        address bound to it"""
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
        thread = threading.Thread(target=message_from_client,args=(conn, addr))
        thread.start()
        print(f"active connections {threading.activeCount() - 1}")


def message_from_client(conn, addr):
    """
    <summary>
    it decodes the string adn broadcasts the message on the client side on the window.
    </summary>
    :param conn: it is the connection to the client side.
    :param addr: it takes the ip address.
    :return: None
    """
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
    """
    <summary>
    it sends the string to the client side.
    </summary>
    :param message: it is the sting to pass to the client side.
    :return: None
    """
    for client in clients:
        client.send(message)



start()     # calling the function.
