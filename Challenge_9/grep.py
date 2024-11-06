import os
import re
import sys

# Function to handle the conversion of \d, \w, and \b
def convert_pattern(pattern):
    pattern = pattern.replace(r'\d', r'[0-9]')
    pattern = pattern.replace(r'\w', r'[a-zA-Z0-9_]')
    return pattern

# Function to handle multiple patterns
def handle_multiple_patterns(patterns):
    combined_pattern = "|".join(patterns)
    return combined_pattern

def grep(pattern, file_path, recursive=False, invert=False, ignore_case=False):
    found_match = False
    # Convert the pattern to handle \d, \w
    pattern = convert_pattern(pattern)
    
    # Check for multiple patterns and combine them
    if " " in pattern or "," in pattern:
        patterns = pattern.split()
        pattern = handle_multiple_patterns(patterns)
    
    try:
        # Handle recursive search
        if recursive:
            for root, dirs, files in os.walk(file_path):
                for file_name in files:
                    full_file_path = os.path.join(root, file_name)
                    with open(full_file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            # Check if the line matches the pattern
                            match_found = re.search(pattern, line, re.IGNORECASE if ignore_case else 0)
                            if (match_found and not invert) or (not match_found and invert):
                                print(f"{full_file_path}: {line}", end='')
                                found_match = True
        else:
            # Non-recursive search
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    match_found = re.search(pattern, line, re.IGNORECASE if ignore_case else 0)
                    if (match_found and not invert) or (not match_found and invert):
                        print(line, end='')
                        found_match = True
    except UnicodeDecodeError:
        print(f"Skipping non-text file: {file_path}")
    except IOError as e:
        print(f"Error opening file {file_path}: {e}")
        sys.exit(1)

    if found_match:
        sys.exit(0)  # Exit code 0 indicates successful match
    else:
        sys.exit(1)  # Exit code 1 indicates no match

# Main function for command-line argument parsing
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python grep.py <pattern> <file_path> [-r] [-v] [-i]")
        sys.exit(1)

    # Initialize variables
    pattern = None
    file_path = None
    recursive = False
    invert = False
    ignore_case = False

    # Parse arguments
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg == "-r":
            recursive = True
        elif arg == "-v":
            invert = True
        elif arg == "-i":
            ignore_case = True
        elif pattern is None:
            pattern = arg
        elif file_path is None:
            file_path = arg

    if pattern is None or file_path is None:
        print("Error: Pattern and file_path must be specified.")
        sys.exit(1)

    # Run grep
    grep(pattern, file_path, recursive, invert, ignore_case)
