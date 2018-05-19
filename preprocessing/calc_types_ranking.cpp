#include <iostream>
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <string>
#include <vector>
#include <unordered_map>
#include <queue>

#define MAX_TYPE 1000000

std::unordered_map<std::string, int> hash;
int cnt;
std::vector<int> graph[MAX_TYPE];
std::vector<int> graph_1[MAX_TYPE];

bool vis[MAX_TYPE];
std::string s[MAX_TYPE];
int T[MAX_TYPE], S[MAX_TYPE];
int in_degree[MAX_TYPE];
int out_degree[MAX_TYPE];


int dp(int x) {
    if (out_degree[x] == 0)
        return T[x] = 0;
    if (T[x] > 0)
        return T[x];
    for (int i = 0; i < graph[x].size(); i++)
        T[x] = std::max(T[x], dp(graph[x][i]) + 1);
    return T[x];
}

int dp_1(int x) {
    if (in_degree[x] == 0)
        return S[x] = 0;
    if (S[x] > 0)
        return S[x];
    for (int i = 0; i < graph_1[x].size(); i++)
        S[x] = std::max(S[x], dp_1(graph_1[x][i]) + 1);
    return S[x];
}


int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: ./calc_types_ranking [taxonomy_file]\n");
        return 0;
    }
    FILE *fin = fopen(argv[1], "r");
    FILE *fout = fopen("../CUTE/data/types_ranking.txt", "w");
    char tmp1[10000], tmp2[10000];
    while (~fscanf(fin, "%s%*s%s", tmp1, tmp2)) {
        if (hash.find(tmp1) == hash.end()) {
            hash[tmp1] = cnt;
            s[cnt] = tmp1;
            cnt++;
        }
        if (hash.find(tmp2) == hash.end()) {
            hash[tmp2] = cnt;
            s[cnt] = tmp2;
            cnt++;
        }
        graph[hash[tmp2]].push_back(hash[tmp1]);
        graph_1[hash[tmp1]].push_back(hash[tmp2]);
        in_degree[hash[tmp1]]++;
        out_degree[hash[tmp2]]++;
    }


    memset(S, 0, sizeof(S));
    memset(T, 0, sizeof(T));

    for (int i = 0; i < cnt; i++)
        if (in_degree[i] == 0) {
            dp(i);
        }

    for (int i = 0; i < cnt; i++)
        if (out_degree[i] == 0) {
            dp_1(i);
        }

        

    for (int i = 0; i < cnt; i++)
        fprintf(fout, "%s %lf\n", s[i].substr(1, s[i].length() - 2).c_str(), 1.0 * (S[i] + 1) / (S[i] + 1 + T[i]));

    return 0;
}
