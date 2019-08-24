#include <stdio.h>
#include <stdbool.h>

void swap(int *num1, int *num2) {
	int temp = *num1;
	*num1 = *num2;
	*num2 = temp;
}

int main(int argc, char *argv[]) {
	int count = 0;
	scanf("%d", &count);
	getchar();
	while (count--) {
		int top[3] = { 0 };
		while (true) {
			int num = 0, ch = 0;
			scanf("%d", &num);
			if (num > top[0] || num > top[1] || num > top[2]) {
				if (top[0] < top[1] && top[0] < top[2]) top[0] = num;
				else if (top[1] < top[2]) top[1] = num;
				else top[2] = num;
			}
			if ((ch = getchar()) && (ch == '\n' || ch == '\r' || ch == EOF)) break;
		}
		if (top[0] < top[1]) swap(top + 0, top + 1);
		if (top[0] < top[2]) swap(top + 0, top + 2);
		if (top[1] < top[2]) swap(top + 1, top + 2);
		printf("%d %d %d\n", top[0], top[1], top[2]);
	}
	return 0;
}