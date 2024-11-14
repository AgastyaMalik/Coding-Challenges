import socket
import threading
import time

def receive_messages(irc_socket):
    try:
        while True:
            response = irc_socket.recv(2048).decode("utf-8")
            if not response:
                break
            print("Server message:", response)
            if response.startswith("PING"):
                # Respond to the PING with a PONG to keep the connection alive
                irc_socket.send(f"PONG {response.split()[1]}\r\n".encode("utf-8"))
                print("Responded to PING.")
    except ConnectionAbortedError:
        print("Connection closed.")
    except OSError:
        print("Socket closed, exiting receive thread.")


def connect_to_irc(server, port, nickname, channel, message):
    irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc_socket.connect((server, port))
    print(f"Connected to server {server} on port {port}")
    
    irc_socket.send(f"NICK {nickname}\r\n".encode("utf-8"))
    irc_socket.send(f"USER {nickname} 0 * :realname\r\n".encode("utf-8"))

    receive_thread = threading.Thread(target=receive_messages, args=(irc_socket,))
    receive_thread.start()
    
    # Wait for server's welcome message before joining the channel
    time.sleep(3)  # Slight delay to ensure registration completes
    irc_socket.send(f"JOIN {channel}\r\n".encode("utf-8"))
    print(f"Joined channel {channel}")
    
    # Send a message to the channel
    irc_socket.send(f"PRIVMSG {channel} :{message}\r\n".encode("utf-8"))
    print(f"Sent message to {channel}: {message}")

    # Wait a moment before quitting
    time.sleep(2)
    irc_socket.send("QUIT :Goodbye!\r\n".encode("utf-8"))
    print("Disconnected from server")
    irc_socket.close()

server = "irc.libera.chat"
port = 6667
nickname = "CCClient"
channel = "#test_channel"
message = "This is a test message before quitting!"

connect_to_irc(server, port, nickname, channel, message)
