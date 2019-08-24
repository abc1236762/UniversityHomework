#include <iostream>
#include <vector>
#include <cstdio>
#include <cstdlib>

using namespace std;

void push_bengla(vector<pair<string, int>> *bengla, const string &num_s,
	const string &&postfix, int &pos, size_t len, bool can_zero) {
	if (pos <= 0) return;
	pos -= len;
	int num = 0;
	if (pos >= 0) num = atoi(num_s.substr((size_t)pos, len).c_str());
	else if (len > 1) num = atoi(num_s.substr((size_t)(pos + 1), len - 1).c_str());
	if (can_zero || num) bengla->emplace_back(postfix, num);
};

vector<pair<string, int>> *cvrt_bengla(const string &num_s) {
	auto bengla = new vector<pair<string, int>>();
	auto pos = (int)num_s.size();
	push_bengla(bengla, num_s, "", pos, 2, atoi(num_s.c_str()) == 0);
	do {
		push_bengla(bengla, num_s, "shata", pos, 1, false);
		push_bengla(bengla, num_s, "hajar", pos, 2, false);
		push_bengla(bengla, num_s, "lakh", pos, 2, false);
		push_bengla(bengla, num_s, "kuti", pos, 2, true);
	} while (pos > 0);
	return bengla;
};

int main(int argc, char **argv) {
	string num_s;
	int n = 0;
	while (getline(cin, num_s)) {
		printf("%4d. ", ++n);
		auto bengla = cvrt_bengla(num_s);
		for (auto i = bengla->rbegin(); i != bengla->rend(); i++) {
			if (i > bengla->rbegin() && i->first == "kuti" && i ->second == 0)
				printf("%s ", i->first.c_str());
			else printf("%d %s ", i->second, i->first.c_str());
		}
		printf("\n");
	}
	return 0;
}