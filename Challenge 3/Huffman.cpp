#include <iostream>
#include <fstream>
#include <unordered_map>
#include <queue>
#include <vector>
#include <string>

using namespace std;

// Define the Node structure for the Huffman tree
struct HuffmanNode {
    char ch;
    int freq;
    HuffmanNode* left;
    HuffmanNode* right;

    HuffmanNode(char character, int frequency) {
        ch = character;
        freq = frequency;
        left = nullptr;
        right = nullptr;
    }
};

// Custom comparator for the priority queue
struct Compare {
    bool operator()(HuffmanNode* a, HuffmanNode* b) {
        return a->freq > b->freq;  // Min-heap based on frequency
    }
};

// Function to build the Huffman Tree based on character frequencies
HuffmanNode* buildHuffmanTree(const unordered_map<char, int>& frequencyMap) {
    priority_queue<HuffmanNode*, vector<HuffmanNode*>, Compare> minHeap;

    // Create leaf nodes for each character
    for (const auto& pair : frequencyMap) {
        HuffmanNode* node = new HuffmanNode(pair.first, pair.second);
        minHeap.push(node);
    }

    // Build the tree by combining two smallest nodes
    while (minHeap.size() > 1) {
        HuffmanNode* left = minHeap.top(); minHeap.pop();
        HuffmanNode* right = minHeap.top(); minHeap.pop();

        // Create a new internal node with a combined frequency
        HuffmanNode* internalNode = new HuffmanNode('\0', left->freq + right->freq);
        internalNode->left = left;
        internalNode->right = right;

        minHeap.push(internalNode);
    }

    return minHeap.top();  // Root of the Huffman Tree
}

// Function to generate Huffman codes for each character
void generateCodes(HuffmanNode* root, const string& code, unordered_map<char, string>& huffmanCodes) {
    if (!root) return;

    // If it's a leaf node, store the code
    if (!root->left && !root->right) {
        huffmanCodes[root->ch] = code;
    }

    generateCodes(root->left, code + "0", huffmanCodes);
    generateCodes(root->right, code + "1", huffmanCodes);
}

// Function to calculate the frequency of each character in the input file
unordered_map<char, int> calculateFrequency(const string &filename) {
    ifstream file(filename);
    unordered_map<char, int> frequencyMap;

    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return frequencyMap;
    }

    char ch;
    while (file.get(ch)) {
        frequencyMap[ch]++;
    }

    file.close();
    return frequencyMap;
}

// Function to write the frequency map and encoded text to the output file
void writeHeaderAndData(ofstream& outputFile, const unordered_map<char, int>& frequencyMap, const string& encodedString) {
    outputFile << frequencyMap.size() << endl;
    for (const auto& pair : frequencyMap) {
        outputFile << pair.first << " " << pair.second << endl;
    }
    outputFile << encodedString << endl;  // Write the encoded text as "0"s and "1"s
}

// Function to encode the input file using Huffman coding
void encodeFile(const string &inputFilename, const string &outputFilename) {
    unordered_map<char, int> frequencyMap = calculateFrequency(inputFilename);
    HuffmanNode* root = buildHuffmanTree(frequencyMap);
    unordered_map<char, string> huffmanCodes;
    generateCodes(root, "", huffmanCodes);

    ofstream outputFile(outputFilename);
    string encodedString = "";
    ifstream inputFile(inputFilename);
    char ch;
    while (inputFile.get(ch)) {
        encodedString += huffmanCodes[ch];  // Convert input characters to encoded bits
    }

    writeHeaderAndData(outputFile, frequencyMap, encodedString);

    inputFile.close();
    outputFile.close();
}

// Function to read the frequency map from the input file
unordered_map<char, int> readHeader(ifstream& inputFile) {
    unordered_map<char, int> frequencyMap;
    int mapSize;
    inputFile >> mapSize;

    char ch;
    int freq;
    for (int i = 0; i < mapSize; ++i) {
        inputFile >> ch >> freq;
        frequencyMap[ch] = freq;
    }
    inputFile.get();  // Read the newline after the frequency map
    return frequencyMap;
}

// Function to decode the encoded string back to the original text
void decodeText(const string &encodedString, const string &outputFilename, HuffmanNode* root) {
    ofstream outputFile(outputFilename);
    HuffmanNode* currentNode = root;
    for (char bit : encodedString) {
        currentNode = (bit == '0') ? currentNode->left : currentNode->right;
        if (!currentNode->left && !currentNode->right) {
            outputFile.put(currentNode->ch);  // Write the decoded character
            currentNode = root;  // Return to root for next sequence
        }
    }

    outputFile.close();
}

// Function to decode the file by reading the encoded data and using the Huffman tree
void decodeFile(const string &inputFilename, const string &outputFilename) {
    ifstream inputFile(inputFilename);
    unordered_map<char, int> frequencyMap = readHeader(inputFile);
    HuffmanNode* root = buildHuffmanTree(frequencyMap);

    string encodedString;
    getline(inputFile, encodedString);  // Read the encoded "0"s and "1"s string

    decodeText(encodedString, outputFilename, root);

    inputFile.close();
}

int main() {
    // Example usage
    string inputFilename = "135-0.txt";  
    string outputFilename = "encoded_output.txt";  
    string decodedFilename = "decoded.txt";  

    // Encode the input file
    encodeFile(inputFilename, outputFilename);

    // Decode the encoded file
    decodeFile(outputFilename, decodedFilename);

    // Calculate file sizes for comparison
    ifstream originalFile(inputFilename, ios::ate);
    ifstream compressedFile(outputFilename, ios::ate);
    streamsize originalSize = originalFile.tellg();
    streamsize compressedSize = compressedFile.tellg();

    // Display the file size comparison
    cout << "Original file size: " << originalSize << " bytes" << endl;
    cout << "Compressed file size: " << compressedSize << " bytes" << endl;

    originalFile.close();
    compressedFile.close();

    return 0;
}
