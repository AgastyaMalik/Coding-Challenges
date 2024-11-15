import socket
import time

def send_command(command, data=""):
    """Helper function to send a command with data and print the response."""
    try:
        # Creating a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 11211))  # Connect to server

        # Prepare the full command with data
        full_command = f"{command}\r\n{data}\r\n"  # Add \r\n before and after the data block
        
        # Send command to server
        client_socket.sendall(full_command.encode('utf-8'))
        
        # Receive response from server
        response = client_socket.recv(1024)
        print(f"Response for '{command} {data}': {response.decode('utf-8')}")
        
    except Exception as e:
        print(f"Error with command '{command} {data}': {e}")
    finally:
        client_socket.close()

# Test commands
commands = [
    ("set test 0 0 4", "data"),  # Test 1: set with data
    ("get test", ""),  # Test 2: get command
    ("add test 0 0 4", "test"),  # Test 3: add with existing key
    ("replace test 0 0 4", "john"),  # Test 4: replace with existing key
    ("get test", ""),  # Test 5: get after replace
    ("append test 0 0 4", "more"),  # Test 6: append
    ("get test", ""),  # Test 7: get after append
    ("prepend test 0 0 4", "send"),  # Test 8: prepend
    ("get test", ""),  # Test 9: get after prepend
    ("add foo 0 0 4", "test"),  # Test 10: add with non-existing key (should fail)
    ("prepend foo 0 0 4", "test"),  # Test 11: prepend with non-existing key (should fail)
]

# Run the commands one by one
for command, data in commands:
    send_command(command, data)
    time.sleep(1)  # Wait for 1 second before sending the next command
