import argparse
import random
import hashlib

def lexicographic_sort(lines, unique=False):
    """Sorts lines lexicographically, optionally removing duplicates."""
    if unique:
        lines = list(set(lines))
    return sorted(lines)

def random_sort(lines, unique=False):
    """Randomly sorts lines by hashing each line with a random hash."""
    if unique:
        lines = list(set(lines))
    
    # Generate a random seed for hashing
    random.seed()
    
    # Use hash of each line with random salt and sort based on these hashes
    hashed_lines = [(line, hashlib.md5((str(random.random()) + line).encode()).hexdigest()) for line in lines]
    hashed_lines.sort(key=lambda x: x[1])  # Sort by the hash value
    return [line for line, _ in hashed_lines]

def main():
    # Set up argument parsing for command line usage
    parser = argparse.ArgumentParser(description="Custom sort tool.")
    parser.add_argument("filename", type=str, help="File to sort")
    parser.add_argument("-u", "--unique", action="store_true", help="Remove duplicate lines")
    parser.add_argument("-R", "--random-sort", action="store_true", help="Randomly sort lines")
    parser.add_argument("-n", type=int, default=5, help="Limit output to top N lines, default is 5")

    args = parser.parse_args()
    
    # Read lines from the file and check if file is read correctly
    try:
        with open(args.filename, 'r') as f:
            lines = f.readlines()
        print(f"File '{args.filename}' read successfully. Number of lines: {len(lines)}")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Choose the sorting function based on command line flags
    if args.random_sort:
        sorted_lines = random_sort(lines, unique=args.unique)
    else:
        sorted_lines = lexicographic_sort(lines, unique=args.unique)

    # Check if sorted_lines has content
    print(f"Number of sorted lines: {len(sorted_lines)}")
    
    # Print the first N lines, based on the -n argument
    for line in sorted_lines[:args.n]:
        print(line.strip())


main()
