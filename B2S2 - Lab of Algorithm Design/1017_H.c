#include <stdio.h>

int main(int argc, char *argv[]) {
	unsigned long long int num = 0;
	while (scanf("%llu", &num) != EOF && !num) {
		if (!(num * 10 % 9)) printf("%llu ", num * 10 / 9 - 1);
		printf("%llu\n", num * 10 / 9);
	}
	return 0;
}