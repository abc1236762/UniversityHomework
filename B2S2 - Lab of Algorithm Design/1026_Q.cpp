#include <iostream>
#include <cstdio>

using namespace std;

int main(int argc, char *argv[]) {
	int n = 0;
	while (cin >> n && n > 0) {
		auto array = new int[n];
		for (int i = 0; i < n; i++) scanf("%d", &array[i]);
		n > 1 ? printf("%d\n", n / 2) : printf("1\n");
		delete []array;
	}
}