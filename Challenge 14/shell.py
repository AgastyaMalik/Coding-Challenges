import os
import subprocess
import platform
import signal
import sys
import readline  # For readline functionality on Windows, using pyreadline

# Signal handler for the shell to ignore SIGINT (CTRL-C) in the main shell
def signal_handler(sig, frame):
    print("\n^Cccsh>", end=' ', flush=True)  # Display the prompt again after CTRL-C

# Run the command in the shell
def run_command(command, input_data=None):
    """Runs a command and handles piping."""
    is_windows = platform.system() == 'Windows'

    # Split the command into arguments
    args = command.split()

    # Handle the 'cat' command replacement for Windows (use 'type' instead)
    if is_windows and args[0] == 'cat':
        args[0] = 'type'  # Replace 'cat' with 'type' on Windows

    try:
        if is_windows:
            # For Windows, use cmd.exe for handling pipes
            if "|" in command:
                # Handle pipes by running the whole command via `cmd /c`
                result = subprocess.run(['cmd', '/c', command], check=True, text=True, capture_output=True, input=input_data)
            else:
                # Single command execution (like `echo`, `type`, etc.)
                result = subprocess.run(['cmd', '/c', command], check=True, text=True, capture_output=True, input=input_data)
        else:
            # For non-Windows (Linux/macOS), run the command normally
            result = subprocess.run(args, check=True, text=True, capture_output=True, input=input_data)

        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: Command '{command}' returned non-zero exit status {e.returncode}\n{e.stderr}"
    except FileNotFoundError:
        return f"Error: '{command}' is not recognized as an internal or external command, operable program or batch file."

# Function to load the history from file
def load_history():
    home_dir = os.path.expanduser("~")
    history_file = os.path.join(home_dir, '.ccsh_history')
    
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

# Function to save the history to file
def save_history(history):
    home_dir = os.path.expanduser("~")
    history_file = os.path.join(home_dir, '.ccsh_history')
    
    with open(history_file, 'w') as file:
        for command in history:
            file.write(f"{command}\n")

# Main function to handle the shell
def main():
    # Load previous command history
    history = load_history()
    
    # Set up the signal handler for SIGINT (CTRL-C) to prevent termination of the shell
    signal.signal(signal.SIGINT, signal_handler)

    is_windows = platform.system() == 'Windows'

    # Enable command history using readline
    # pyreadline automatically stores history, so no need to manually manage this part
    # But we will handle saving history manually

    while True:
        try:
            # Display the prompt with the current working directory
            cwd = os.getcwd()  # Get the current working directory
            command = input(f"{cwd} ccsh> ").strip()  # Show full current directory path
        except KeyboardInterrupt:
            # Ignore the interruption and allow the shell to continue
            continue  # This will ignore the CTRL-C and re-display the prompt
        
        # Add command to history
        if command != '':
            history.append(command)
            readline.add_history(command)  # Add to readline history for scrolling with arrows
        # Save history to file on exit
        if command == 'exit':
            print("Exiting shell...")
            save_history(history)  # Save the command history to disk
            break
        
        # Handle the built-in commands: cd, pwd, and history
        if command.startswith('cd'):
            args = command.split()
            if len(args) > 1:
                new_dir = args[1].replace('/', '\\') if is_windows else args[1]
                try:
                    os.chdir(new_dir)
                except FileNotFoundError:
                    print(f"Error: No such file or directory: '{new_dir}'")
                except PermissionError:
                    print(f"Error: Permission denied: '{new_dir}'")
            else:
                print("Error: 'cd' requires a directory argument.")
            continue  # Skip running external commands after handling cd

        elif command == 'pwd':
            print(os.getcwd())  # Print the current working directory
            continue  # Skip running external commands after handling pwd

        elif command == 'history':
            # Print the command history
            print("\nCommand History:")
            for i, cmd in enumerate(history[-10:]):  # Display last 10 commands
                print(f"{i+1}. {cmd}")
            continue  # Skip running external commands after handling history

        # Handle pipe by splitting the command at '|'
        if '|' in command:
            # Split the command by pipes into individual commands
            commands = command.split('|')
            prev_output = None

            for cmd in commands:
                cmd = cmd.strip()  # Remove any extra whitespace around each command
                # Run the command, pass the previous output as input if it's not the first one
                if prev_output is None:
                    output = run_command(cmd)
                else:
                    output = run_command(cmd, prev_output)  # Pass output of previous command as input for the next one
                prev_output = output  # Store the output for the next command in the chain

            print(prev_output)  # Print the final output of the last command
        else:
            # If there's no pipe, run the command normally
            output = run_command(command)
            print(output)

# Start the shell
if __name__ == '__main__':
    main()
