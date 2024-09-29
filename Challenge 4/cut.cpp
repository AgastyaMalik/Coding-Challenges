#include <algorithm>
#include <fstream>
#include <iostream>
#include <ostream>
#include <string>
#include <vector>
using namespace std;
const char LINE_DELIMITER = '\n';

void cut(string filename, vector<int> columns, char delimiter) {
    ifstream file{filename};
    if (!file.good()) {
        cout << "\nfile not found\n";
        return;
    }

    if (columns.size() == 0) {
        string line2;
        getline(file, line2);
        
    }
    sort(columns.begin(), columns.end());

    vector<int> skips{};
    for (int i = columns.size() - 1; i >= 0; --i) {
        int distance = 0;
        if (i == 0) {
            distance = columns.at(0) - 1;
        } else {
            distance = columns.at(i) - columns.at(i-1) - 1;
        }

        skips.push_back(distance);
    }

    reverse(skips.begin(), skips.end());

    while (!file.eof()) {
        vector<vector<char>> output{};
        for (int i = 0; i < skips.size(); ++i) {

            int toSkip = skips.at(i);
            for (int j = 0; j < toSkip; ++j) {
                file.ignore(256, delimiter);
            }

            // take chars from the stream until delimiter
            char ch = file.get();
            vector<char> word = {};
            while( ch != delimiter ) {
                word.push_back(ch);
                ch = file.get();
            }

            output.push_back(word);
        }
        for (int i = 0; i < output.size(); ++i) {
            for (auto ch : output.at(i)) {
                cout << ch;
            }
            if (i != output.size() - 1) {
                cout << delimiter;
            }
        }
        cout << endl;
        file.ignore(1024, LINE_DELIMITER);
    }
};

int main (int argc, char *argv[]) {
    using namespace literals;
    string command = argv[1];
    vector<string> args(argv + 1, argv + argc);
    vector<int> columns{};

    char delimiter = ',';

    for (auto arg : args) {
        int index = arg.find('-');
        if (index != -1) {
            char command_type = arg.at(index + 1);
            string command_value = arg.substr(index + 2);

            if (command_type == 'f') {
                size_t index = 0;
                string command;
                while ((index = command_value.find(',')) != string::npos) {
                    command = command_value.substr(0, index);
                    columns.push_back(stoi(command));
                    command_value.erase(0, index + 1);
                }

                if (index == string::npos) {
                    columns.push_back(stoi(command_value));
                }
            }
            if (command_type == 'd' && command_value.length()) {

                delimiter = command_value.at(0);
                if (delimiter == 't') {
                    delimiter = '\t';
                }
            }
        }
    }

    string filename = args.back();
    if (command == "-h"sv || command == "--help"sv) {
        cout << "help text here" << endl;
        return 0;
    }
    cut(filename, columns, delimiter);

    return 0;
}