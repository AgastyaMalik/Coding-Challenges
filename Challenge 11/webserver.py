import os
import socket
import mimetypes
from urllib.parse import unquote

HOST, PORT = '127.0.0.1', 80
WWW_DIR = 'D:\\vscode\\codes\\python\\Coding_Challenges\\Challange_11'

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Allow up to 5 queued connections
    print(f"Server started on {HOST}:{PORT}")

    while True:  # Infinite loop to keep the server running
        client_socket, client_address = server_socket.accept()
        with client_socket:
            print(f"Connection from {client_address} established.")
            try:
                # Receive the request data
                request_data = client_socket.recv(1024).decode()
                request_line = request_data.splitlines()[0]
                method, path, _ = request_line.split()

                # Handle only GET requests; otherwise, respond with 405
                if method != "GET":
                    response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\nMethod Not Allowed"
                    client_socket.sendall(response.encode())
                    continue

                # Decode URL and prevent directory traversal attacks
                path = unquote(path)
                if path == "/":
                    path = "/index.html"
                file_path = os.path.join(WWW_DIR, path.strip("/"))

                # Ensure file path is within WWW_DIR
                if not file_path.startswith(WWW_DIR):
                    response = "HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain\r\n\r\nForbidden"
                    client_socket.sendall(response.encode())
                    continue

                # Check if the requested file exists
                if os.path.exists(file_path):
                    # Read the file contents as binary
                    with open(file_path, 'rb') as file:
                        body = file.read()

                    # Determine content type based on file extension
                    content_type, _ = mimetypes.guess_type(file_path)
                    if content_type is None:
                        content_type = 'application/octet-stream'  # Default binary type

                    # Create the HTTP response with headers
                    response_headers = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: {content_type}\r\n"
                        f"Content-Length: {len(body)}\r\n\r\n"
                    )
                    response = response_headers.encode() + body
                else:
                    # Return a 404 response if the file is not found
                    body = "Page not found.".encode()
                    response_headers = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {len(body)}\r\n\r\n"
                    )
                    response = response_headers.encode() + body

                # Send the complete response
                client_socket.sendall(response)

            except Exception as e:
                # Handle unexpected server errors
                error_body = f"Internal Server Error: {e}".encode()
                response_headers = (
                    "HTTP/1.1 500 Internal Server Error\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(error_body)}\r\n\r\n"
                )
                response = response_headers.encode() + error_body
                client_socket.sendall(response)

            finally:
                client_socket.close()
