#include <iostream>
#include <map>
#include <cstdio>

using namespace std;

int main(int argc, char **argv) {
	int n = 0, data = 0;
	while (cin >> n) {
		while (n--) {
			cin >> data;
			if (data > 1) {
				map<int, int> q;
				for (int i = 9; i > 1 && data != 1; i--) {
					while (!(data % i)) {
						q[i]++;
						data /= i;
					}
				}
				if (data == 1) {
					for (auto &i : q) {
						for (int j = 0; j < i.second; j++)
							printf("%d", i.first);
					}
				} else printf("-1");
			} else if (data == 1) printf("1");
			else printf("0");
			printf("\n");
		}
	}
	return 0;
}