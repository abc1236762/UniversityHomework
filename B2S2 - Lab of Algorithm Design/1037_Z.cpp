#include <iostream>
#include <map>
#include <sstream>
#include <cstdio>

using namespace std;

int main(int argc, char **argv) {
	int n = 0;
	while (cin >> n && getchar()) {
		map<string, int> m;
		while (n--) {
			string line, str;
			getline(cin, line);
			istringstream iss(line);
			iss >> str;
			if (m.find(str) == m.end()) m[str] = 0;
			m[str]++;
		}
		for (auto &p : m) printf("%s %d\n", p.first.c_str(), p.second);
	}
	return 0;
}