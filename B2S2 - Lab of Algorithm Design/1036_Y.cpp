#include <iostream>
#include <cctype>
#include <cstdio>

using namespace std;

int main(int argc, char **argv) {
	string num_o;
	while (getline(cin, num_o)) {
		if (num_o == "0") break;
		int judge11 = 0;
		string num;
		for (size_t i = 0; i < num_o.size(); i++)
			if (isdigit(num_o[i])) {
				judge11 += i % 2 ? num_o[i] - '0' : -(num_o[i] - '0');
				num += num_o[i];
			}
		if (judge11 % 11) printf("%s is not a multiple of 11.\n", num.c_str());
		else printf("%s is a multiple of 11.\n", num.c_str());
	}
	return 0;
}
