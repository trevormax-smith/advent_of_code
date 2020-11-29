#include <iostream>
#include <vector>
#include <fstream>
#include <string>

using namespace std;

vector<string> parse_file(string filename) {
    ifstream input_file;
    input_file.open(filename, ios::in);
    string line;
    vector<string> file_contents;

    if (input_file.is_open())
    {
        while( getline(input_file, line) ){
            file_contents.push_back(line);
        }
        input_file.close();
    }
    return file_contents;
}


int what_floor(string test_instruction) {
    int floor = 0;
    for (const char& c: test_instruction){
        switch(c) {
            case '(':
                floor++;
                break;
            case ')':
                floor--;
                break;
            default:
                break;
        }
    }
    return floor;
}


int first_in_basement_at(string test_instruction) {
    int floor = 0;
    for (int i = 0; i < test_instruction.size(); i++){
        char& c = test_instruction[i];
        switch(c) {
            case '(':
                floor++;
                break;
            case ')':
                floor--;
                break;
            default:
                break;
        }
        if (floor < 0){
            return i + 1;
        }
    }
    return 0;
}


int main()
{

    string test_instruction {"(()))("};
    int floor_num = what_floor(test_instruction);
    cout << "TESTS" << endl;
    cout << "Floor number " << floor_num << endl;
    cout << "First in basement " << first_in_basement_at(test_instruction) << endl;
    cout << endl;

    vector<string> instructions = parse_file("./inputs/day01.txt");

    // for (auto i = instructions.begin(); i != instructions.end(); ++i){
    //     cout << *i << endl << endl;
    // }

    string instruction = *instructions.begin();
    cout << "REAL THING" << endl;
    cout << "Floor number: " << what_floor(instruction) << endl;
    cout << "First in basement: " << first_in_basement_at(instruction) << endl;
}
