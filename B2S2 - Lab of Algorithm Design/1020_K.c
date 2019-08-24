#include <stdio.h>
#include <math.h>

int main(int argc, char *argv[]) {
	int start = 0, end = 0;
	while (scanf("%d%d", &start, &end) != EOF && (start || end))
		printf("%d\n", (int)sqrt(end) - (int)ceil(sqrt(start)) + 1);
	return 0;
}