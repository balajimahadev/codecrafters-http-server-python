# Uncomment this to pass the first stage
import socket
import threading
import os
import argparse

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory")
    args = parser.parse_args()
    directory = args.directory
    
    while True:
        client_socket, client_address = server_socket.accept() # wait for client
        threading.Thread(target=process_request, args=(client_socket,client_address, directory)).start()
        

def process_request(client_socket, client_address, directory):
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
        response = f"HTTP/1.1 200 OK \r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\n{content}".encode()
    elif path == '/':
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    
    elif method == 'GET' and path.startswith('/files/'):
        # Extract the filename from the path
        filename = path.split('/')[-1]

        # Construct the absolute path to the file
        filepath = os.path.join(directory, filename)

        # Check if the file exists
        if os.path.isfile(filepath):
            # If the file exists, send a 200 OK response with file contents
            with open(filepath, 'rb') as file:
                file_contents = file.read()
                
            header = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/octet-stream\r\n"
                f"Content-Length: {len(file_contents)}\r\n\r\n"
            ).encode()

            response = header+file_contents
        else:
            # If the file doesn't exist, send a 404 Not Found response
            response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n".encode()

    # Check if the method is POST and the path starts with "/files/"
    elif method == 'POST' and path.startswith('/files/'):
        # Extract the filename from the path
        filename = path.split('/')[-1]

        # Extract the file contents from the request body
        file_contents = request_lines[-1].encode('utf-8')

        # Construct the absolute path to save the file
        filepath = os.path.join(directory, filename)

        # Save the file contents to the specified directory
        with open(filepath, 'wb') as file:
            file.write(file_contents)

        # Send a 201 Created response
        response = "HTTP/1.1 201 Created\r\n\r\n".encode()

    elif path == '/user-agent':
        response = f"HTTP/1.1 200 OK \r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\n{user_agent}".encode()
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    # Send the response
    client_socket.sendall(response)

if __name__ == "__main__":
    main()
