#include <iostream>
#include <string>
#include <cctype>
#include <sstream>
#include <vector>
#include <map>

// Function declarations
bool isValidJsonString(const std::string &str);
bool isValidJsonBoolean(const std::string &str);
bool isValidJsonNull(const std::string &str);
bool isValidJsonNumber(const std::string &str);
bool isValidJsonValue(const std::string &value);
std::string trim(const std::string &str);
bool parseJsonValue(const std::string &value);
bool parseJson(const std::string &json);
bool parseJsonArray(const std::string &jsonArray);

// Check if a string is a valid JSON string
bool isValidJsonString(const std::string &str) {
    return str.length() >= 2 && str.front() == '"' && str.back() == '"';
}

// Check if a string is a valid JSON boolean
bool isValidJsonBoolean(const std::string &str) {
    return str == "true" || str == "false";
}

// Check if a string is a valid JSON null
bool isValidJsonNull(const std::string &str) {
    return str == "null";
}

// Check if a string is a valid JSON number
bool isValidJsonNumber(const std::string &str) {
    if (str.empty()) return false;

    size_t i = 0;
    bool hasDigits = false;
    bool hasDecimalPoint = false;

    // Check for optional leading sign
    if (str[i] == '-' || str[i] == '+') i++;

    while (i < str.length()) {
        char c = str[i];
        if (isdigit(c)) {
            hasDigits = true;
        } else if (c == '.' && !hasDecimalPoint) {
            hasDecimalPoint = true;
        } else if (c == '.' && hasDecimalPoint) {
            return false; // Invalid: More than one decimal point
        } else if ((c == 'e' || c == 'E') && hasDigits) {
            i++;
            if (i < str.length() && (str[i] == '+' || str[i] == '-')) i++;
            if (i == str.length() || !isdigit(str[i])) return false;
        } else {
            return false; // Invalid character
        }
        i++;
    }

    return hasDigits; // Return true if there are digits
}

// Check if a value is valid JSON (string, boolean, null, number, object, or array)
bool isValidJsonValue(const std::string &value) {
    return isValidJsonString(value) || isValidJsonBoolean(value) || 
           isValidJsonNull(value) || isValidJsonNumber(value) || 
           value.front() == '{' || value.front() == '['; // Allow objects or arrays
}

// Trim whitespace from a string
std::string trim(const std::string &str) {
    size_t start = str.find_first_not_of(" \t\n\r");
    size_t end = str.find_last_not_of(" \t\n\r");
    return (start == std::string::npos || end == std::string::npos) ? "" : str.substr(start, end - start + 1);
}

// Parse a JSON value (including objects and arrays)
bool parseJsonValue(const std::string &value) {
    std::string trimmedValue = trim(value);
    if (trimmedValue.front() == '{') {
        return parseJson(trimmedValue); // Handle JSON object
    } else if (trimmedValue.front() == '[') {
        return parseJsonArray(trimmedValue); // Handle JSON array
    }
    return isValidJsonValue(trimmedValue);
}

// Parse a JSON array
bool parseJsonArray(const std::string &jsonArray) {
    std::string trimmedJsonArray = trim(jsonArray);
    if (trimmedJsonArray.front() != '[' || trimmedJsonArray.back() != ']') {
        std::cerr << "Invalid JSON: Missing opening or closing bracket" << std::endl;
        return false;
    }

    std::string content = trimmedJsonArray.substr(1, trimmedJsonArray.length() - 2);
    std::istringstream stream(content);
    std::string value;

    // Parse each value in the array
    while (std::getline(stream, value, ',')) {
        if (!parseJsonValue(trim(value))) {
            return false; // Return false immediately if any value is invalid
        }
    }

    return true; // Valid JSON array
}

// Parse a JSON object
bool parseJson(const std::string &json) {
    std::string trimmedJson = trim(json);
    if (trimmedJson.front() != '{' || trimmedJson.back() != '}') {
        std::cerr << "Invalid JSON: Missing opening or closing brace" << std::endl;
        return false;
    }

    std::string content = trimmedJson.substr(1, trimmedJson.length() - 2);
    std::istringstream stream(content);
    std::string pair;

    // Parse each key-value pair
    while (std::getline(stream, pair, ',')) {
        size_t colonPos = pair.find(':');
        if (colonPos == std::string::npos) {
            std::cerr << "Invalid JSON: Missing colon between key and value" << std::endl;
            return false;
        }

        std::string key = trim(pair.substr(0, colonPos));
        std::string value = trim(pair.substr(colonPos + 1));

        // Check if the key is a valid JSON string
        if (!isValidJsonString(key)) {
            std::cerr << "Invalid JSON: Key is not a valid string" << std::endl;
            return false;
        }

        // Check if the value is valid
        if (!parseJsonValue(value)) {
            return false; // Return false immediately if value is invalid
        }
    }

    return true; // Valid JSON object
}

// Main function
int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <json-string>" << std::endl;
        return 1;
    }

    std::string json = argv[1];
    if (parseJson(json)) {
        std::cout << "Valid JSON" << std::endl;
        return 0; // valid
    } else {
        std::cout << "Invalid JSON" << std::endl;
        return 1; // invalid
    }
}
