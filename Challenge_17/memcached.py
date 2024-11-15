import socket
import time

store = {}  # In-memory key-value store

def process_request(data):
    """
    Process client requests like 'set', 'get', 'add', 'replace', 'append', and 'prepend'.
    """
    lines = data.split("\r\n")
    if not lines:
        return "ERROR\r\n"

    command = lines[0].split()
    if command[0] == "set":
        if len(command) < 5:
            return "CLIENT_ERROR bad command line format\r\n"
        
        key, flags, exptime, length = command[1:5]
        value = lines[1] if len(lines) > 1 else ""
        
        # Calculate expiry time
        exptime = int(exptime)
        if exptime < 0:
            expiry_time = time.time()  # Immediately expired
        elif exptime == 0:
            expiry_time = 0  # Never expires
        else:
            expiry_time = time.time() + exptime  # Expire after <exptime> seconds
        
        # Store the value and expiry time
        store[key] = {'value': value, 'expiry_time': expiry_time}
        
        return "STORED\r\n"

    elif command[0] == "get":
        if len(command) < 2:
            return "CLIENT_ERROR bad command line format\r\n"
        
        key = command[1]
        
        if key in store:
            item = store[key]
            
            # Check if the item has expired
            if item['expiry_time'] != 0 and time.time() > item['expiry_time']:
                del store[key]  # Remove expired item
                return "END\r\n"  # Expired item
            
            value = item['value']
            return f"VALUE {key} 0 {len(value)}\r\n{value}\r\nEND\r\n"
        else:
            return "END\r\n"
    
    elif command[0] == "add":
        if len(command) < 5:
            return "CLIENT_ERROR bad command line format\r\n"
        
        key, flags, exptime, length = command[1:5]
        value = lines[1] if len(lines) > 1 else ""
        
        # Check if the key already exists
        if key in store:
            return "NOT_STORED\r\n"
        
        # Calculate expiry time
        exptime = int(exptime)
        if exptime < 0:
            expiry_time = time.time()  # Immediately expired
        elif exptime == 0:
            expiry_time = 0  # Never expires
        else:
            expiry_time = time.time() + exptime  # Expire after <exptime> seconds
        
        # Store the value and expiry time
        store[key] = {'value': value, 'expiry_time': expiry_time}
        
        return "STORED\r\n"

    elif command[0] == "replace":
        if len(command) < 5:
            return "CLIENT_ERROR bad command line format\r\n"
        
        key, flags, exptime, length = command[1:5]
        value = lines[1] if len(lines) > 1 else ""
        
        # Check if the key exists
        if key not in store:
            return "NOT_STORED\r\n"
        
        # Calculate expiry time
        exptime = int(exptime)
        if exptime < 0:
            expiry_time = time.time()  # Immediately expired
        elif exptime == 0:
            expiry_time = 0  # Never expires
        else:
            expiry_time = time.time() + exptime  # Expire after <exptime> seconds
        
        # Replace the value and expiry time
        store[key] = {'value': value, 'expiry_time': expiry_time}
        
        return "STORED\r\n"

    elif command[0] == "append":
        if len(command) < 5:
            return "CLIENT_ERROR bad command line format\r\n"
        
        key, flags, exptime, length = command[1:5]
        value = lines[1] if len(lines) > 1 else ""
        
        # Check if the key exists
        if key not in store:
            return "NOT_STORED\r\n"
        
        # Append to the existing value
        store[key]['value'] += value
        
        # Calculate expiry time
        exptime = int(exptime)
        if exptime < 0:
            expiry_time = time.time()  # Immediately expired
        elif exptime == 0:
            expiry_time = 0  # Never expires
        else:
            expiry_time = time.time() + exptime  # Expire after <exptime> seconds
        
        store[key]['expiry_time'] = expiry_time
        
        return "STORED\r\n"

    elif command[0] == "prepend":
        if len(command) < 5:
            return "CLIENT_ERROR bad command line format\r\n"
        
        key, flags, exptime, length = command[1:5]
        value = lines[1] if len(lines) > 1 else ""
        
        # Check if the key exists
        if key not in store:
            return "NOT_STORED\r\n"
        
        # Prepend to the existing value
        store[key]['value'] = value + store[key]['value']
        
        # Calculate expiry time
        exptime = int(exptime)
        if exptime < 0:
            expiry_time = time.time()  # Immediately expired
        elif exptime == 0:
            expiry_time = 0  # Never expires
        else:
            expiry_time = time.time() + exptime  # Expire after <exptime> seconds
        
        store[key]['expiry_time'] = expiry_time
        
        return "STORED\r\n"

    else:
        return "ERROR\r\n"

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen(1)
    print(f"Server started on port {port}. Waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection received from {addr}")
        with client_socket:
            data = client_socket.recv(1024).decode("utf-8")
            print(f"Received data: {data}")
            if not data:
                break

            response = process_request(data)
            client_socket.sendall(response.encode("utf-8"))

if __name__ == "__main__":
    start_server(11211)
