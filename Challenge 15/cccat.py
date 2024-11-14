import sys

def print_file_contents(filename, number_lines=False, number_non_blank=False):
    try:
        if filename == '-':
            lines = sys.stdin.readlines()
        else:
            with open(filename, 'r') as file:
                lines = file.readlines()

        line_count = 1
        for line in lines:
            if number_lines or (number_non_blank and line.strip()):
                print(f"{line_count}  {line}", end='')
                line_count += 1 if line.strip() else 0
            else:
                print(line, end='')

    except FileNotFoundError:
        print(f"File {filename} not found.")

if __name__ == "__main__":
    number_lines = '-n' in sys.argv
    number_non_blank = '-b' in sys.argv
    files = [arg for arg in sys.argv[1:] if arg not in ('-n', '-b')]
    
    if files:
        for filename in files:
            print_file_contents(filename, number_lines, number_non_blank)
    else:
        print("Please specify a file to read.")
