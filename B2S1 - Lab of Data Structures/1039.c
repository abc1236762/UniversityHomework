#include <stdio.h>

int main() {
	int Readers = 0, Books = 0;
	while (scanf("%d%d", &Readers, &Books) != EOF) {
		int i = 0, j = 0, Table[Readers];
		for (i = 0; i < Readers; i++) scanf("%d", Table + i);
		for (i = 0; i < Readers; i++) {
			int Count = 0;
			for (j = 0; j < Readers; j++) if (Table[i] == Table[j]) Count++;
			Count == 1 ? printf("BeiJu\n") : printf("%d\n", Count - 1);
		}
	}
	return 0;
}