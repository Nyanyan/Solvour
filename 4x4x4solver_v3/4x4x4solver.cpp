#include <iostream>
#include <algorithm>
#include <vector>
#include <cstdio>
#include <chrono>
#include <utility>
#include <string>
//#include <cmath>
#include <fstream>
#include <sstream>
#include <array>

#define rep(i, n, m) for(int i = (n); (i) < (m); (i)++)
#define len(arr) sizeof(arr) / sizeof(*arr)

using namespace std;

const array<int, 8> cp_d = {0, 1, 2, 3, 4, 5, 6, 7};
const array<int, 8> co_d = {0, 0, 0, 0, 0, 0, 0, 0};
const array<int, 24> ep_d = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23};
const array<int, 24> ce_d = {0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5};


long long fac[25];

//                            0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
const string move_candidate[36] = {"R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"};
const int twist_to_idx[36] = {0, 1, 2, 3, 4, 5, 6, 7, 8, -1, -1, -1, 9, 10, 11, 12, 13, 14, 15, 16, 17, -1, -1, -1, 18, 19, 20, 21, 22, 23, 24, 25, 26, -1, -1, -1};

const vector<vector<int>> successor = {
    {0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14, 15, 16, 17, 18, 19, 20,             24, 25, 26, 27, 28, 29, 30, 31, 32            }, // phase 0
    {0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            }, // phase 1
    {   1,       4,       7,               12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            }, // phase 2
    {   1,       4,       7,               12, 13, 14,             18, 19, 20,                 25,         28,         31,               }, // phase 3
    {0,    2,          6,    8,            12, 13, 14,             18, 19, 20,             24,     26,             30,     32            }, // phase 4
    {   1,                7,               12, 13, 14,             18, 19, 20,                 25,                     31                }  // phase 5
    };

vector<vector<vector<int>>> prunning;
int prun_len[6] = {1, 7, 3, 2, 2, 3};


int move_ce_phase0[735471][27];
int move_ce_phase1_fbud[12870][27];
int move_ce_phase1_rl[70][27];
int move_ce_phase2[343000][27];
int move_ep[255024][27];
int move_ep_phase3[40320][27];


void init(){
    fac[0] = 1;
    rep(i, 1, 25) fac[i] = fac[i - 1] * i;
    //rep(i, 0, 25) cout << fac[i] << ' ';
}
/*
int cmb(int n, int r){
    return int(fac[n] / fac[r] / fac[n - r]);
}
*/

unsigned long long cmb(long long a,long long b){
    unsigned long long cmb=1;
    long long c=min(b,a-b);
    long long d=2;
    for(long long i=a-c+1  ;i<=a  ;i++){
        cmb*=i;
        while(cmb%d==0 and d<=c){
            cmb/=d;
            d++;
        }
    }
    return cmb;
}
/*
unsigned long long cmb(int n, int r) {
  std::vector<std::vector<long long>> v(n + 1,std::vector<long long>(n + 1, 0));
  for (int i = 0; i < v.size(); i++) {
    v[i][0] = 1;
    v[i][i] = 1;
  }
  for (int j = 1; j < v.size(); j++) {
    for (int k = 1; k < j; k++) {
      v[j][k] = (v[j - 1][k - 1] + v[j - 1][k]);
    }
  }
  return v[n][r];
}
*/

class Cube{
    public:
    array<int, 8> Cp;
    array<int, 8> Co;
    array<int, 24> Ep;
    array<int, 24> Ce;
    void set(array<int, 8> cp, array<int, 8> co, array<int, 24> ep, array<int, 24> ce);
    int idx_ce_phase0();
    array<int, 8> move_cp(int twist);
    array<int, 8> move_co(int twist);
    array<int, 24> move_ep(int twist);
    array<int, 24> move_ce(int twist);
};

void Cube::set(array<int, 8> cp, array<int, 8> co, array<int, 24> ep, array<int, 24> ce){
    rep(i, 0, 8) this->Cp[i] = cp[i];
    rep(i, 0, 8) this->Co[i] = co[i];
    rep(i, 0, 24) this->Ep[i] = ep[i];
    rep(i, 0, 24) this->Ce[i] = ce[i];
}

array<int, 8> Cube::move_cp(int twist){
    int surface[6][4] = {{3, 1, 7, 5}, {0, 2, 4, 6}, {0, 1, 3, 2}, {4, 5, 7, 6}, {2, 3, 5, 4}, {1, 0, 6, 7}};
    array<int, 8> res;
    rep(i, 0, 8) res[i] = this->Cp[i];
    int type = twist / 6;
    int amount = twist % 3;
    rep(i, 0, 4) res[surface[type][(i + amount + 1) % 4]] = this->Cp[surface[type][i]];
    return res;
}

array<int, 8> Cube::move_co(int twist){
    int surface[6][4] = {{3, 1, 7, 5}, {0, 2, 4, 6}, {0, 1, 3, 2}, {4, 5, 7, 6}, {2, 3, 5, 4}, {1, 0, 6, 7}};
    int pls[4] = {2, 1, 2, 1};
    array<int, 8> res;
    rep(i, 0, 8) res[i] = this->Co[i];
    int type = twist / 6;
    int amount = twist % 3;
    rep(i, 0, 4){
        res[surface[type][(i + amount + 1) % 4]] = this->Co[surface[type][i]];
        if(int(type / 2) != 1 && amount != 1){
            res[surface[type][(i + amount + 1) % 4]] += pls[(i + amount + 1) % 4];
            res[surface[type][(i + amount + 1) % 4]] %= 3;
        }
    }
    return res;
}

array<int, 24> Cube::move_ep(int twist){
    vector<vector<vector<int>>> surface = {
        {{3, 12, 19, 10}, {2, 13, 18, 11}}, // R
        {{3, 12, 19, 10}, {2, 13, 18, 11}, {4, 1, 20, 17}},  // Rw
        {{7, 8, 23, 14}, {6, 9, 22, 15}}, // L
        {{7, 8, 23, 14}, {6, 9, 22, 15}, {0, 5, 16, 21}}, // Lw
        {{0, 2, 4, 6}, {1, 3, 5, 7}}, // U
        {{0, 2, 4, 6}, {1, 3, 5, 7}, {15, 12, 11, 8}}, // Uw
        {{16, 18, 20, 22}, {17, 19, 21, 23}}, // D
        {{16, 18, 20, 22}, {17, 19, 21, 23}, {9, 10, 13, 14}}, // Dw
        {{5, 11, 17, 9}, {4, 10, 16, 8}}, // F
        {{5, 11, 17, 9}, {4, 10, 16, 8}, {6, 3, 18, 23}}, // Fw
        {{1, 15, 21, 13}, {0, 14, 20, 12}}, // B
        {{1, 15, 21, 13}, {0, 14, 20, 12}, {2, 7, 22, 19}} // Bw
    };
    array<int, 24> res;
    rep(i, 0, 24) res[i] = this->Ep[i];
    int type = twist / 3;
    int amount = twist % 3;
    rep(i, 0, surface[type].size()){
        rep(j, 0, 4) res[surface[type][i][(j + amount + 1) % 4]] = this->Ep[surface[type][i][j]];
    }
    return res;
}


array<int, 24> Cube::move_ce(int twist){
    vector<vector<vector<int>>> surface = {
        {{8, 9, 10, 11}}, // R
        {{8, 9, 10, 11}, {2, 12, 22, 6}, {1, 15, 21, 5}}, // Rw
        {{16, 17, 18, 19}}, // L
        {{16, 17, 18, 19}, {0, 4, 20, 14}, {3, 7, 23, 13}}, // Lw
        {{0, 1, 2, 3}}, // U
        {{0, 1, 2, 3}, {13, 9, 5, 17}, {12, 8, 4, 16}}, // Uw
        {{20, 21, 22, 23}}, // D
        {{20, 21, 22, 23}, {7, 11, 15, 19}, {6, 10, 14, 18}}, // Dw
        {{4, 5, 6, 7}}, // F
        {{4, 5, 6, 7}, {3, 8, 21, 18}, {2, 11, 20, 17}}, // Fw
        {{12, 13, 14, 15}}, // B
        {{12, 13, 14, 15}, {1, 16, 23, 10}, {0, 19, 22, 9}} // Bw
    };
    array<int, 24> res;
    rep(i, 0, 24) res[i] = this->Ce[i];
    int type = twist / 3;
    int amount = twist % 3;
    rep(i, 0, surface[type].size()){
        rep(j, 0, 4) res[surface[type][i][(j + amount + 1) % 4]] = this->Ce[surface[type][i][j]];
    }
    return res;
}

int Cube::idx_ce_phase0(){
    int res = 0;
    int cnt = 0;
    rep(i, 0, 23){
        if(this->Ce[i] == 2 || this->Ce[i] == 4){
            res += cmb(23 - i, 8 - cnt);
            cnt++;
            if(cnt == 8 || i - cnt == 15) break;
        }
    }
    return res;
}



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

void get_move_ce_phase0(){
    ifstream ifs("move_table/move_ce_phase0.csv");
    string line;
    rep(lin, 0, 735471) {
        getline(ifs, line);
        vector<string> strvec = split(line, ',');
        rep(i, 0, strvec.size()) move_ce_phase0[lin][i] = int(stoi(strvec.at(i)));
    }
}

void get_move_ce_phase1_rl(){
    ifstream ifs("move_table/move_ce_phase1_rl.csv");
    string line;
    rep(lin, 0, 70) {
        getline(ifs, line);
        vector<string> strvec = split(line, ',');
        rep(i, 0, strvec.size()) move_ce_phase1_rl[lin][i] = int(stoi(strvec.at(i)));
    }
}

void get_prunning(){
    rep(phase, 0, 1){
        prunning.push_back({});
        ifstream ifs("prun_table/prunning" + to_string(phase) + ".csv");
        string line;
        rep(lin, 0, prun_len[phase]) {
            prunning[phase].push_back({});
            getline(ifs, line);
            vector<string> strvec = split(line, ',');
            rep(i, 0, strvec.size()) prunning[phase][lin].push_back(int(stoi(strvec.at(i))));
        }
    }
}


vector<int> solution;
vector<int> path;

int face(int twist){
    return int(twist / 3);
}

int axis(int twist){
    return int(twist / 12);
}

int wide(int twist){
    return face(twist) % 2;
}

vector<int> puzzle_initialize(int phase, Cube puzzle){
    if(phase == 0) return (vector<int>){puzzle.idx_ce_phase0()};
}

vector<int> move_arr(int phase, vector<int> puzzle_arr, int twist){
    if(phase == 0) return (vector<int>){move_ce_phase0[puzzle_arr[0]][twist_to_idx[twist]]};
}

int distance(int phase, vector<int> puzzle_arr){
    int res = 0;
    rep(i, 0, prun_len[phase]) res += prunning[phase][i][puzzle_arr[i]];
    return res;
}

bool phase_search(int phase, vector<int> puzzle_arr, int depth){
    if(depth == 0){
        if(distance(phase, puzzle_arr) == 0) return true;
        else return false;
    } else {
        if(distance(phase, puzzle_arr) <= depth){
            int l1_twist = -10;
            int l2_twist = -10;
            int l3_twist = -10;
            int siz = path.size();
            if(siz >= 1) l1_twist = path[siz - 1];
            if(siz >= 2) l2_twist = path[siz - 2];
            if(siz >= 3) l3_twist = path[siz - 3];
            rep(idx, 0, successor[phase].size()){
                int twist = successor[phase][idx];
                if(face(twist) == face(l1_twist) || (axis(twist) == axis(l1_twist) && axis(l1_twist) == axis(l2_twist) && axis(l2_twist) == axis(l3_twist)) || (axis(twist) == axis(l1_twist) && wide(twist) == wide(l1_twist) && wide(l1_twist) == 1))
                    continue;
                vector<int> n_puzzle_arr = move_arr(phase, puzzle_arr, twist);
                path.push_back(twist);
                if(phase_search(phase, n_puzzle_arr, depth - 1)) return true;
                path.pop_back();
            }
            return false;
        }
    }
}

void solver(Cube puzzle){
    rep(phase, 0, 1){
        cout << "phase " << phase << " depth ";
        chrono::system_clock::time_point  s, e;
        s = chrono::system_clock::now();
        rep(depth, 0, 30){
            vector<int> puzzle_arr = puzzle_initialize(phase, puzzle);
            //cout << "puzzle_arr ";
            //rep(i, 0, puzzle_arr.size()) cout << puzzle_arr[i] << ' ';
            cout << endl;
            cout << depth << " ";
            path = {};
            if(phase_search(phase, puzzle_arr, depth)){
                cout << endl;
                rep(i, 0, path.size()){
                    int twist = path[i];
                    solution.push_back(twist);
                    puzzle.set(puzzle.move_cp(twist), puzzle.move_co(twist), puzzle.move_ep(twist), puzzle.move_ce(twist));
                    cout << move_candidate[twist] << " ";
                }
                cout << endl;
                e = chrono::system_clock::now();
                double elap = chrono::duration_cast<chrono::milliseconds>(e-s).count();
                cout << "phase time: " << elap << "ms" << endl;
                break;
            }
        }
    }
}


int main() {
    init();
    cout << "init done" << endl;
    get_move_ce_phase0();
    cout << "move_ce_phase0 done" << endl;
    get_prunning();
    cout << "prunning done" << endl;
    Cube puzzle;
    puzzle.set(cp_d, co_d, ep_d, ce_d);
    vector<int> scramble;
    string scramble_str;
    cout << "input scramble: "; 
    cin >> scramble_str;
    istringstream spl(scramble_str);
    string s;
    while(spl >> s){
        rep(i, 0, 36){
            if(move_candidate[i] == s){
                scramble.push_back(i);
                break;
            }
        }
    }
    rep(i, 0, scramble.size()){
        int twist = scramble[i];
        puzzle.set(puzzle.move_cp(twist), puzzle.move_co(twist), puzzle.move_ep(twist), puzzle.move_ce(twist));
    }
    chrono::system_clock::time_point  start, end;
    start = chrono::system_clock::now();
    solver(puzzle);
    end = chrono::system_clock::now();
    double elapsed = chrono::duration_cast<chrono::milliseconds>(end-start).count();
    cout << "all time: " << elapsed << "ms" << endl;
    return 0;
}