# Uncomment this to pass the first stage
import socket

from whatthepatch import parse_patch


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept() # wait for client

    # Read data from the connection
    data = client_socket.recv(1024)

    # Decode the data from bytes to string
    request_str = data.decode('utf-8')

    # Split the request by lines
    request_lines = request_str.split('\r\n')

    # Extract the path from the request line
    request_line = request_lines[0]
    method, path, _ = request_line.split()

    # Parse the path to extract the random string
    random_string = parse_patch(path)

    # Prepare the response body with the parsed random string
    response_body = random_string.encode('utf-8')


    # Print the path
    print('Requested path:', response_body)


# Determine the response status and message based on the path
    if path == '/':
        #response_status = b"HTTP/1.1 200 OK\r\n\r\n"
        response_status = b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(response_body), response_body)
    else:
        response_status = b"HTTP/1.1 404 Not Found\r\n\r\n"

    # Send the response
    client_socket.sendall(response_status)

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    main()
