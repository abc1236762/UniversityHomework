#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>

int get_each_num(char ch) {
	if (isdigit(ch)) return ch - '0';
	else if (isupper(ch)) return ch - 'A' + 10;
	else if (islower(ch)) return ch - 'a' + 10 + 26;
	return -1;
}

bool is_divisible(char *num_s, int base) {
	int num = 0, each_num = 0;
	do {
		if ((each_num = get_each_num(*num_s)) >= 0) {
			if (each_num + 1 > base) return false;
			num = (num + each_num) % (base - 1) * base;
		}
	} while (*++num_s);
	return !num;
}

int main(int argc, char *argv[]) {
	char num_s[128] = "";
	while (fgets(num_s, 128, stdin)) {
		int result = 0;
		for (int i = 2; i <= 62 && !result; i++) if (is_divisible(num_s, i)) result = i;
		result ? printf("%d\n", result) : printf("such number is impossible!\n");
	}
	return 0;
}