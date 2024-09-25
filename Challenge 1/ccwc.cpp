#include <iostream>
#include <fstream>
#include <sstream>  // For splitting strings into words
#include <string>

using namespace std;

// Function to count bytes from a file stream
int countBytes(ifstream& file) {
    file.seekg(0, ios::end);  // Move to the end of the file
    return file.tellg();  // Get the size in bytes
}

// Function to count lines from an input stream
int countLines(istream& input) {
    string line;
    int lineCount = 0;
    while (getline(input, line)) {  // Read each line
        lineCount++;  // Increment line count for each line read
    }
    return lineCount;  // Return the total line count
}

// Function to count words from an input stream
int countWords(istream& input) {
    string line;
    int wordCount = 0;
    while (getline(input, line)) {
        istringstream iss(line);  // Create a string stream for the line
        string word;
        while (iss >> word) {  // Extract words from the line
            wordCount++;  // Increment word count for each word
        }
    }
    return wordCount;  // Return the total word count
}

// Function to count characters from an input stream
int countCharacters(istream& input) {
    char ch;
    int charCount = 0;

    // Read the input character by character
    while (input.get(ch)) {
        charCount++;  // Increment character count for each character read
    }

    return charCount;  // Return the total character count
}

int main(int argc, char* argv[]) {
    // Check if at least one argument (option) is provided
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <option> [<filename>]" << endl;
        return 1;  // Exit with error
    }

    string option = argv[1];  // Get the option
    ifstream file;  // File stream

    // Check if a filename is provided
    if (argc == 3) {
        string filename = argv[2];  // Get the filename
        file.open(filename);  // Attempt to open the file
        if (!file.is_open()) {  // Check if the file opened successfully
            cerr << "Error: could not open file: " << filename << endl;
            return 1;  // Exit with error
        }
    }

    // Determine the input source
    istream& input = (argc == 3) ? file : cin;  // Use file or standard input

    // Check if the option is valid
    if (option != "-c" && option != "-l" && option != "-w" && option != "-m") {
        cerr << "Invalid option! Use -c, -l, -w, or -m." << endl;
        return 1;  // Exit with error
    }

    // Handle specific options
    if (option == "-c") {
        int byteCount = countBytes(file);  // Call countBytes only if file is provided
        if (argc == 3 && byteCount != -1) {
            cout << byteCount << " bytes in " << argv[2] << endl;  // Output byte count
        } else if (argc == 2) {
            cout << byteCount << " bytes from standard input" << endl;
        }
    } else if (option == "-l") {
        int lineCount = countLines(input);
        cout << lineCount << " lines" << endl;  // Output line count
    } else if (option == "-w") {
        int wordCount = countWords(input);
        cout << wordCount << " words" << endl;  // Output word count
    } else if (option == "-m") {
        int charCount = countCharacters(input);
        cout << charCount << " characters" << endl;  // Output character count
    }

    // Close the file if it was opened
    if (file.is_open()) {
        file.close();
    }

    return 0;  // Exit successfully
}
