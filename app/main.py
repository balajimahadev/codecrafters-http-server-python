# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept() # wait for client

    # Read data from the connection
    data = client_socket.recv(1024)
    # Respond with HTTP/1.1 200 OK
    response = b"HTTP/1.1 200 OK\r\n\r\n"

    # Send the response
    client_socket.sendall(response)

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    main()
