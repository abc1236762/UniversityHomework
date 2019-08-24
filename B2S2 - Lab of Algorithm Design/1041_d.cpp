// Wrong Answer

#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <cfloat>

using namespace std;

int round0p01xy(int a, int b) {
	double xy0p01 = (abs(pow(a, 2) - pow(b, 2)) / 4) * 0.01;
	return (int)(fabs(xy0p01 - floor(xy0p01) - 0.5) < DBL_EPSILON ? ceil(xy0p01) : round(xy0p01));
}

int main(int argc, char **argv) {
	int n = 0;
	while (cin >> n) {
		while (n--) {
			int nums[3] = { 0 }, k = 0;
			bool is_passed = false;
			cin >> nums[0] >> nums[1] >> nums[2];
			for (int i = 0; i < 3; i++) {
				for (int j = i + 1; j < 3; j++) {
					double xy = abs(pow(nums[i], 2) - pow(nums[j], 2)) / 4;
					if ((i == 1 && j == 2) || (i == 2 && j == 1)) k = 0;
					else if ((i == 2 && j == 0) || (i == 0 && j == 2)) k = 1;
					else if ((i == 0 && j == 1) || (i == 1 && j == 0)) k = 2;
					is_passed = round0p01xy(nums[i], nums[j]) == abs(nums[k]);
					if (is_passed) goto finished;
				}
			}
			finished:
			is_passed ? printf("Yes\n") : printf("No\n");
		}
	}
}