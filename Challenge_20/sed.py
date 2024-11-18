import re
import sys

# Function to handle sed commands
def sed_substitute(command, filename, output_file=None, line_range=None, in_place=False):
    if command == "-n":
        if line_range:  # If there's a line range or pattern
            if '/' in line_range:  # This means it's a pattern search.
                pattern = line_range.strip("/")
                print_lines_matching_pattern(filename, pattern)
            else:  # This means it's a line range.
                # Remove any quotes and then split the range
                line_range = line_range.strip("'\"")  # Remove quotes if they exist
                start, end = map(int, line_range.split(','))
                print_lines_in_range(filename, start, end)
        else:
            print("No range or pattern provided for -n.")
    elif command == "G":
        # Double space the file
        double_space_file(filename)
    elif command.startswith("s/"):
        # Handle substitution command: s/pattern/replacement/
        substitution = command[1:]  # Remove the 's/' part
        pattern, replacement, flags = extract_pattern_and_replacement(substitution)
        substitute_in_file(filename, pattern, replacement, flags, in_place)
    elif command == "-d":
        # Handle command to delete trailing blank lines
        delete_trailing_blank_lines(filename)
    elif command == "-i":
        # In-place editing (modify the file directly)
        if len(sys.argv) < 4:
            print("Usage: python sed.py -i s/pattern/replacement/ filename")
            sys.exit(1)
        substitution = sys.argv[2]  # The substitution pattern
        filename = sys.argv[3]      # The filename
        pattern, replacement, flags = extract_pattern_and_replacement(substitution)
        substitute_in_file(filename, pattern, replacement, flags, in_place=True)
    else:
        print(f"Invalid command. Usage: python sed.py [-n range | s/pattern/replacement/ | G | -i] filename")

# Function to extract the pattern and replacement from the substitution command
def extract_pattern_and_replacement(substitution):
    parts = substitution.split('/', 2)  # Split into pattern, replacement, and flags
    if len(parts) < 3:
        print("Invalid substitution format. Expected: s/pattern/replacement/g")
        sys.exit(1)
    pattern = parts[0]
    replacement = parts[1]
    flags = parts[2] if len(parts) > 2 else ''
    return pattern, replacement, flags

# Function to print lines that match a given pattern
def print_lines_matching_pattern(filename, pattern):
    try:
        with open(filename, 'r') as file:
            for line in file:
                if re.search(pattern, line):
                    print(line, end='')
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")

# Function to print lines within a specified range
def print_lines_in_range(filename, start, end):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for i in range(start-1, min(end, len(lines))):  # Adjust for 0-based indexing
                print(lines[i], end='')
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")

# Function to double space the content of the file (G command)
def double_space_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                print(line, end='')  # Print the line
                print()  # Print a blank line after each line
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")

# Function to perform substitution in a file (s/pattern/replacement/)
def substitute_in_file(filename, pattern, replacement, flags, in_place=False):
    try:
        with open(filename, 'r') as file:
            content = file.read()

        # Perform substitution
        if 'g' in flags:  # Global replacement flag
            updated_content = re.sub(pattern, replacement, content)
        else:
            updated_content = re.sub(pattern, replacement, content, count=1)  # Single replacement

        # If in_place is True, overwrite the original file
        if in_place:
            with open(filename, 'w') as file:
                file.write(updated_content)
            print(f"In-place modification applied to {filename}")
        else:
            # Print the updated content or write to an output file
            if output_file:
                with open(output_file, 'w') as output:
                    output.write(updated_content)
            else:
                print(updated_content)

        # Print content for debugging purposes
        print("\nUpdated Content of the File:\n")
        print(updated_content)

    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")

# Function to delete trailing blank lines
def delete_trailing_blank_lines(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        # Strip trailing blank lines
        while lines and lines[-1].strip() == "":
            lines.pop()  # Remove the last line if it's empty
        
        # Print the updated content or write to an output file
        for line in lines:
            print(line, end='')  # Output the remaining lines (no trailing blanks)

    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")

if __name__ == "__main__":
    # Initialize the output_file variable (if not defined)
    output_file = None

    # Check if the correct number of arguments were passed
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python sed.py [-n range | s/pattern/replacement/ | G | -i] filename [output_file]")
        sys.exit(1)

    # Extract the command
    command = sys.argv[1]

    # Set the 'in_place' flag for -i option
    in_place = command == "-i"

    # Handle the -n option with range/pattern or s/pattern/replacement/
    if command == "-n":
        # Extract the range or pattern and the filename
        if len(sys.argv) < 4:
            print("Usage: python sed.py -n [range] filename")
            sys.exit(1)
        line_range = sys.argv[2]  # Range or pattern to search for
        filename = sys.argv[3]
    elif command.startswith("s/"):
        # Handle substitution command
        if len(sys.argv) < 4:
            print("Usage: python sed.py s/pattern/replacement/ filename")
            sys.exit(1)
        line_range = None
        filename = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
    elif command == "G":
        # Handle the double spacing command (G)
        if len(sys.argv) < 3:
            print("Usage: python sed.py G filename")
            sys.exit(1)
        line_range = None
        filename = sys.argv[2]
    elif command == "-d":
        # Handle the delete trailing blank lines command (-d)
        if len(sys.argv) < 3:
            print("Usage: python sed.py -d filename")
            sys.exit(1)
        line_range = None
        filename = sys.argv[2]
    elif command == "-i":
        # In-place editing (modify the file directly)
        if len(sys.argv) < 4:
            print("Usage: python sed.py -i s/pattern/replacement/ filename")
            sys.exit(1)
        line_range = None
        filename = sys.argv[3]  # The filename comes here
        substitution = sys.argv[2]  # The substitution pattern
        pattern, replacement, flags = extract_pattern_and_replacement(substitution)
        substitute_in_file(filename, pattern, replacement, flags, in_place=True)
    else:
        print(f"Invalid command. Usage: python sed.py [-n range | s/pattern/replacement/ | G | -i] filename")
        sys.exit(1)

    # Debugging the received arguments
    print(f"Debug: command={command}, filename={filename}, output_file={output_file}, line_range={line_range}")

    # Run the appropriate sed operation
    sed_substitute(command, filename, output_file, line_range, in_place)
