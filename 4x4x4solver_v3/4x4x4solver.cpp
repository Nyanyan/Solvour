#include <iostream>
#include <algorithm>
#include <vector>
#include <cstdio>
#include <chrono>
#include <utility>
#include <string>
#include <cmath>
#include <fstream>
#include <sstream>

#define rep(i, n, m) for(int i = (n); (i) < (m); (i)++)
#define len(arr) sizeof(arr) / sizeof(*arr)

using namespace std;

//                 0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
string move_candidate[36] = {"R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"};
int twist_to_idx[36] = {0, 1, 2, 3, 4, 5, 6, 7, 8, -1, -1, -1, 9, 10, 11, 12, 13, 14, 15, 16, 17, -1, -1, -1, 18, 19, 20, 21, 22, 23, 24, 25, 26, -1, -1, -1};

vector<vector<int>> successor = 
    {
    vector<int>{0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14, 15, 16, 17, 18, 19, 20,             24, 25, 26, 27, 28, 29, 30, 31, 32            }, // phase 0
    vector<int>{0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            }, // phase 1
    vector<int>{   1,       4,       7,               12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            }, // phase 2
    vector<int>{   1,       4,       7,               12, 13, 14,             18, 19, 20,                 25,         28,         31,               }, // phase 3
    vector<int>{0,    2,          6,    8,            12, 13, 14,             18, 19, 20,             24,     26,             30,     32            }, // phase 4
    vector<int>{   1,                7,               12, 13, 14,             18, 19, 20,                 25,                     31                }  // phase 5
    };


int move_ce_phase0[735471][27];
int move_ce_phase1_fbud[12870][27];
int move_ce_phase1_rl[70][27];
int move_ce_phase2[343000][27];

vector<string> split(string& input, char delimiter)
{
    istringstream stream(input);
    string field;
    vector<string> result;
    while (getline(stream, field, delimiter)) {
        result.push_back(field);
    }
    return result;
}

void get_move_arr(){
    ifstream ifs("move_table/move_ce_phase1_rl.csv");
    string line;
    rep(lin, 0, 70) {
        getline(ifs, line);
        vector<string> strvec = split(line, ',');
        rep(i, 0, strvec.size()) move_ce_phase1_rl[lin][i] = int(stoi(strvec.at(i)));
    }
}

int main() {
    return 0;
}