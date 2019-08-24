#include <iostream>

using namespace std;

int main(int argc, char **argv) {
	int n = 0, m = 0;
	while (cin >> n) {
		while (n--) {
			cin >> m;
			int result = 1;
			while (m % 3 == 0) m /= 3, result *= 3;
			while (m % 5 == 0) m /= 5, result *= 5;
			cout << result << endl;
		}
	}
	return 0;
}