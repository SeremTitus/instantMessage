import socket
import threading
import time

def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to a known address (doesn't send data)
        s.connect(('10.0.0.1', 1))

        # Get the local IP address from the socket
        local_ip = s.getsockname()[0]

        return local_ip
    except socket.error as e:
        print("Error:", e)
        return None

receive_ip_online = ""
def is_online(server_ip, server_port):
    global receive_ip_online
    start_time = time.time()
    while receive_ip_online != server_ip:
        send_message(server_ip, server_port,"[are_you_online?]")
        if (time.time() - start_time) > 10:
            return False
    receive_ip_online = ""
    return True

def receive_messages(server_socket,server_port):
    global receive_ip_online
    while True:
        client_socket, client_address = server_socket.accept()
        message = client_socket.recv(1024).decode("utf-8")
        if message == "[are_you_online?]":
            send_message(client_address[0], server_port, "[am_online]")
        elif message == "[am_online]":
            receive_ip_online = client_address[0]
        else:        
            print(f"Received message from {client_address[0]}: {message}")
        client_socket.close()

def send_message(server_ip, server_port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.send(message.encode("utf-8"))
    client_socket.close()

def main():
    print("Your IP is : " + get_local_ip())
    # Set up the server socket
    server_ip = "0.0.0.0"  # Listen on all available interfaces
    server_port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    # Start the thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(server_socket,server_port))
    receive_thread.start()

    while True:
        # Get the IP address of the recipient
        recipient_ip = input("Enter the IP address of the recipient: ")
        
        if len(recipient_ip) > 0:
            #check if online
            if not is_online(recipient_ip, server_port):
                print(recipient_ip + " is offline. Try later")
                continue

            # Get the message to send
            message = input("Enter your message: ")

            # Send the message
            if len(message) < 0:
                message = "[empty message]"
            try:
                send_message(recipient_ip, server_port, message)
            except:
                print("failed to send message, check ip")

if __name__ == "__main__":
    main()
