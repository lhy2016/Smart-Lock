import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname(socket.gethostname())
server_address = (HOST, 9876)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print('received "%s"' % data)
            if data:
                while True:
                    userInput = input("what do you want to say?\n")
                    if (userInput == "exit"):
                        break
                    connection.sendall(bytes(userInput,"utf-8"))
                    print("\n Sending back '", userInput,"'.......\n")
            else:
                print('no more data from', client_address)
            
    finally:
        # Clean up the connection
        connection.close()