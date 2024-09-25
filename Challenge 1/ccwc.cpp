#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// Function to count lines, words, characters, and bytes in a single pass
void countAll(istream& input, int& lineCount, int& wordCount, int& byteCount, int& charCount) {
    string line;
    lineCount = 0;
    wordCount = 0;
    byteCount = 0;
    charCount = 0;

    while (getline(input, line)) {
        lineCount++;                // Increment line count
        byteCount += line.size() + 1; // Count bytes (including newline)
        charCount += line.size();    // Count characters (excluding newline)

        bool inWord = false;
        for (char c : line) {
            if (isspace(c)) {
                if (inWord) wordCount++; // End of a word
                inWord = false;
            } else {
                inWord = true;
            }
        }
        if (inWord) wordCount++;  // Count the last word if line ends without space
    }
}

// Main function to handle argument parsing and file processing
int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " [-c|-l|-w|-m] [filename]" << endl;
        return 1;
    }

    bool hasOption = false;
    string option = "";
    string filename = "";
    ifstream file;

    // Check if first argument is an option (starts with '-')
    if (argv[1][0] == '-') {
        hasOption = true;
        option = argv[1];
    }

    // Determine the filename based on whether an option is present
    if (hasOption) {
        if (argc == 3) {
            filename = argv[2];  // Filename provided after the option
        } else {
            cerr << "Error: No filename provided after option." << endl;
            return 1;
        }
    } else {
        filename = argv[1];  // First argument is the filename (no option)
    }

    // Open file if a filename is provided
    if (!filename.empty()) {
        file.open(filename);
        if (!file.is_open()) {
            cerr << "Error: could not open file: " << filename << endl;
            return 1;
        }
    }

    // Input stream: either the file or standard input
    istream& input = (filename.empty()) ? cin : file;

    // Count all necessary metrics in a single pass
    int lineCount = 0, wordCount = 0, byteCount = 0, charCount = 0;
    countAll(input, lineCount, wordCount, byteCount, charCount);

    // Output based on the option
    if (hasOption) {
        if (option == "-c") {
            cout << byteCount << " bytes" << endl;
        } else if (option == "-l") {
            cout << lineCount << " lines" << endl;
        } else if (option == "-w") {
            cout << wordCount << " words" << endl;
        } else if (option == "-m") {
            cout << charCount << " characters" << endl;
        } else {
            cerr << "Invalid option! Use -c, -l, -w, or -m." << endl;
            return 1;
        }
    } else {
        // Default case: print lines, words, and bytes
        cout << lineCount << " " << wordCount << " " << byteCount << " ";
        if (!filename.empty()) {
            cout << filename << endl;  // If a filename is provided
        } else {
            cout << "from standard input" << endl;  // If reading from standard input
        }
    }

    // Close the file if it was opened
    if (file.is_open()) {
        file.close();
    }

    return 0;
}
