# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)


    while True:
        client_socket, client_address = server_socket.accept() # wait for client

        # Read data from the connection
        data = client_socket.recv(1024)

        # Decode the data from bytes to string
        request_str = data.decode('utf-8')

        # Split the request by lines
        request_lines = request_str.split('\r\n')

        # Extract the User-Agent header
        user_agent = None
        for line in request_lines:
            if line.startswith('User-Agent:'):
                user_agent = line.split(': ')[1]
                print(user_agent)
                break

        # Extract the path from the request line
        request_line = request_lines[0]
        method, path, _ = request_line.split()


        #Determine the response status and message based on the path
        if "echo" in path:
            content = path[6:]
            response_status = f"HTTP/1.1 200 OK \r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\n{content}".encode()

        elif path == '/':
            response_status = b"HTTP/1.1 200 OK\r\n\r\n"

        elif path == '/user-agent':
            response_status = f"HTTP/1.1 200 OK \r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\n{user_agent}".encode()
        else:
            response_status = b"HTTP/1.1 404 Not Found\r\n\r\n"

        # Send the response
        client_socket.sendall(response_status)

        # Close the connection
        client_socket.close()


if __name__ == "__main__":
    main()
