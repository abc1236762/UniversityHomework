#include <stdio.h>
#include <string.h>
#include <stdbool.h>

typedef struct _pair {
	char ch;
	int count;
} pair;

#define swap(x, y) ((x) ^= (y)), ((y) ^= (x)), ((x) ^= (y))

void sel_sort(pair *table, int len) {
	for (int i = 0; i < len - 1; i++) {
		int min_i = i;
		for (int j = i + 1; j < len; j++)
			if ((table[j].count == table[min_i].count && table[j].ch > table[min_i].ch) ||
				table[j].count < table[min_i].count) min_i = j;
		if (i != min_i) {
			swap(table[i].ch, table[min_i].ch);
			swap(table[i].count, table[min_i].count);
		}
	}
}

int main(int argc, char *argv[]) {
	char string[1001] = "";
	while (gets(string)) {
		pair table[256] = { { '\0', 0 } };
		for (int i = 0; i < 256; i++) table[i].ch = (char)i;
		for (int i = 0; i < strlen(string); i++) table[string[i]].count++;
		sel_sort(table, 256);
		for (int i = 0; i < 256; i++) if (table[i].count > 0) printf("%d %d\n", table[i].ch, table[i].count);
		printf("\n");
	}
	return 0;
}