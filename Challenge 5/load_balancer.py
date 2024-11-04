import socket
import argparse
import time
import threading
import requests

# Set up command-line arguments
parser = argparse.ArgumentParser(description="HTTP Load Balancer")
parser.add_argument("--port", type=int, default=80, help="Port to listen on")
parser.add_argument("--health-check-period", type=int, default=10, help="Health check period in seconds")
parser.add_argument("--health-check-url", type=str, default="/health", help="Health check URL path")
args = parser.parse_args()

# Load command-line arguments for health check
health_check_period = args.health_check_period
health_check_url = args.health_check_url

# Define backend servers for load balancing
backend_servers = [('localhost', 8081), ('localhost', 8082)]
current_backend_index = 0
healthy_backends = backend_servers.copy()  # Start with all servers as healthy

# Function for health checking backend servers
def health_check():
    global healthy_backends
    while True:
        for backend in backend_servers:
            host, port = backend
            health_check_endpoint = f"http://{host}:{port}{health_check_url}"
            try:
                response = requests.get(health_check_endpoint)
                if response.status_code == 200:
                    # Add to healthy_backends if not already there
                    if backend not in healthy_backends:
                        healthy_backends.append(backend)
                        print(f"Server {backend} is now healthy.")
                else:
                    # Remove from healthy_backends if the response is not 200
                    if backend in healthy_backends:
                        healthy_backends.remove(backend)
                        print(f"Server {backend} is unhealthy.")
            except requests.ConnectionError:
                # Remove from healthy_backends if connection fails
                if backend in healthy_backends:
                    healthy_backends.remove(backend)
                    print(f"Server {backend} is down.")
        
        time.sleep(health_check_period)  # Wait for the specified period before the next check

# Function to get the next available backend server
def get_next_backend():
    global current_backend_index
    if not healthy_backends:  # If no healthy servers, return None or handle accordingly
        print("No healthy backends available.")
        return None

    backend = healthy_backends[current_backend_index]
    current_backend_index = (current_backend_index + 1) % len(healthy_backends)
    return backend

# Function to handle client requests
def handle_client(client_socket):
    try:
        # Receive the HTTP request from the client
        request_data = client_socket.recv(1024).decode()

        # Choose a backend server to forward the request
        backend = get_next_backend()
        if backend is None:
            client_socket.sendall(b"HTTP/1.1 503 Service Unavailable\r\n\r\nNo healthy backend servers.")
            return

        backend_host, backend_port = backend

        # Send the request to the selected backend server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_socket:
            backend_socket.connect((backend_host, backend_port))
            backend_socket.sendall(request_data.encode())

            # Receive the response from the backend server and forward it to the client
            while True:
                response_data = backend_socket.recv(4096)
                if not response_data:
                    break
                client_socket.sendall(response_data)

    except ConnectionError:
        print("Error: Unable to forward request to the backend.")
        client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\nBackend server unavailable.")
    finally:
        client_socket.close()

# Function to start the load balancer server
def start_load_balancer(port=80):
    # Start the health check in a separate thread
    health_thread = threading.Thread(target=health_check, daemon=True)
    health_thread.start()

    # Create and bind the socket
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind(('localhost', port))
    load_balancer_socket.listen(5)
    print(f"Load Balancer listening on port {port}...")

    while True:
        client_socket, client_address = load_balancer_socket.accept()
        print(f"Received request from {client_address}")

        # Handle client requests in a new thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

start_load_balancer(args.port)
