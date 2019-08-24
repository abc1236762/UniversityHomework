#include <stdio.h>
#include <stdbool.h>

int main(int argc, char *argv[]) {
	int n = 0, t = 0;
	while (scanf("%d", &n) != EOF) {
		int arr[n];
		bool table[20000] = { false }, is_b2 = true;
		for (int i = 0; i < n; i++) scanf("%d", arr + i);
		for (int i = 0; i < n && is_b2; i++) {
			for (int j = 0; j <= i && is_b2; j++) {
				is_b2 = !table[arr[i] + arr[j]];
				table[arr[i] + arr[j]] = true;
			}
		}
		printf("Case #%d: ", ++t);
		is_b2 ? printf("It is a B2-Sequence.\n\n") : printf("It is not a B2-Sequence.\n\n");
	}
	return 0;
}