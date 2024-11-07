import sys

def uniq(input_file, output_file=None, count=False, repeated=False, unique_only=False):
    previous_line = None
    previous_count = 0
    output = []

    input_stream = open(input_file, 'r') if input_file != '-' else sys.stdin

    def process_line(line, line_count):
        """Process each line based on options, preparing it for output."""
        if unique_only and line_count == 1:
            return f"{line}" if not count else f"{line_count} {line}"
        elif repeated and line_count > 1:
            return f"{line}" if not count else f"{line_count} {line}"
        elif not unique_only and not repeated:
            return f"{line}" if not count else f"{line_count} {line}"
        return None

    try:
        with input_stream as file:
            for line in file:
                line = line.rstrip()
                if line == previous_line:
                    previous_count += 1
                else:
                    if previous_line is not None:
                        # Output previous line if it meets criteria
                        output_line = process_line(previous_line, previous_count)
                        if output_line:
                            output.append(output_line)
                    # Update to new line
                    previous_line = line
                    previous_count = 1

            # Handle the last line in the file
            if previous_line is not None:
                output_line = process_line(previous_line, previous_count)
                if output_line:
                    output.append(output_line)

        # Output results
        if output_file:
            with open(output_file, 'w') as out_file:
                for line in output:
                    out_file.write(line + '\n')
        else:
            for line in output:
                print(line)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")

#handle command-line arguments
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python uniq.py <input_file> [-c] [-d] [-u] [output_file]")
    else:
        input_file = sys.argv[1]
        output_file = None
        count = False
        repeated = False
        unique_only = False

        # Loop through arguments to find flags
        for arg in sys.argv[2:]:
            if arg == "-c":
                count = True
            elif arg == "-d":
                repeated = True
            elif arg == "-u":
                unique_only = True
            else:
                output_file = arg

        uniq(input_file, output_file, count, repeated, unique_only)
