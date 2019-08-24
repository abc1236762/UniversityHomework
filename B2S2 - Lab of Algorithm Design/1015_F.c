#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
	char n1[11] = "", n2[11] = "";
	while (scanf("%s%s", n1, n2) != EOF) {
		if (!strcmp(n1, "0") && !strcmp(n2, "0")) break;
		size_t max_len = strlen(n1) > strlen(n2) ? strlen(n1) : strlen(n2);
		int carry_c = 0, carry_n = 0;
		for (int i = 1; i <= max_len; i++) {
			if (i <= strlen(n1)) carry_n += n1[strlen(n1) - i] - '0';
			if (i <= strlen(n2)) carry_n += n2[strlen(n2) - i] - '0';
			carry_n /= 10;
			if (carry_n > 0) carry_c++;
		}
		if (!carry_c) printf("No carry operation.\n");
		else if (carry_c == 1) printf("1 carry operation.\n");
		else printf("%d carry operations.\n", carry_c);
	}
	return 0;
}