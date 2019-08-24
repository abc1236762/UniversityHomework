#include <stdio.h>

int main(int argc, char *argv[]) {
	unsigned int s1 = 0, s2 = 0;
	while (scanf("%u%u", &s1, &s2) != EOF) printf("%u\n", s1 > s2 ? s1 - s2 : s2 - s1);
	return 0;
}