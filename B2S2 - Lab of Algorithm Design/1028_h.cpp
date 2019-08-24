#include <iostream>
#include <cstdio>

using namespace std;

int main(int argc, char **argv) {
	int n = 0;
	while (cin >> n) {
		for (int i = 0; i < n; i++) {
			int left = 0, right = 0, result = 0;
			cin >> left >> right;
			for (int j = left; j <= right; j++) if (j % 2) result += j;
			printf("Case %d: %d\n", i+1, result);
		}
	}
	return 0;
}