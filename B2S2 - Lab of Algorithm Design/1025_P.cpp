#include <iostream>
#include <algorithm>
#include <cstdio>

using namespace std;

struct customer {
	int id, level;
};

bool sort_level(customer x, customer y) {
	return x.level > y.level;
}

int main(int argc, char *argv[]) {
	int n = 0;
	while (cin >> n && n > 0) {
		auto customers = new customer[n];
		auto reserve = new int[n];
		for (int i = 0; i < n; i++) {
			customers[i].id = i;
			scanf("%d", &customers[i].level);
		}
		stable_sort(customers, customers + n, sort_level);
		for (int i = 0; i < n; i++) reserve[customers[i].id] = i;
		for (int i = 0; i < n; i++) printf("%d ", reserve[i] + 1);
		cout << endl;
		delete []customers;
		delete []reserve;
	}
	return 0;
}