#include <cstdio>
#include <iostream>

using namespace std;

int main() {
	int l = 0, x = 0;
	while ((cin >> l >> x) && ((l != 0) && (x != 0))) {
		auto p = new int[l + 1];
		for (int i = 0; i <= l; i++) p[i] = 0;
		p[0] = 1;
		for (int i = 1; i <= l; i++) for (int j = 1; j <= x && j <= i; j++) p[i] = (p[i] + p[i - j]) % 10000007;
		printf("%d\n", p[l]);
		delete []p;
	}
	return 0;
}
