#include <iostream>
#include <cstdio>

using namespace std;

int main(int argc, char **argv) {
	int table[10][10][10] = { 0 };
	for (int i = 0; i <= 9; i++) {
		for (int j = 0; j <= 9; j++) {
			for (int k = 0; k <= 9; k++) {
				table[i][j][k] = 222 * (i + j + k) - (100 * i + 10 * j + k);
			}
		}
	}
	int n = 0, sum = 0;
	while (cin >> n) {
		while (n--) {
			cin >> sum;
			for (int i = 0; i <= 9; i++) {
				for (int j = 0; j <= 9; j++) {
					for (int k = 0; k <= 9; k++) {
						if (table[i][j][k] == sum) {
							printf("%d %d %d\n", i, j, k);
							goto finished;
						}
					}
				}
			}
			finished:;
		}
	}
	return 0;
}
