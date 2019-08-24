#include <stdio.h>

int MinIndex(const int *Array, int Start, int Size) {
	int Min = Start, i = 0;
	for (i = Start; i < Size; i++) if (Array[i] < Array[Min]) Min = i;
	return Min;
}

int main() {
	int Count = 0;
	while (scanf("%d", &Count) != EOF) {
		int Array[Count], i = 0, j = 0;
		for (i = 0; i < Count; i++)scanf("%d", Array + i);
		for (i = 0; i < Count; i++) {
			j = MinIndex(Array, i, Count);
			if (i != j) {
				int Temp = Array[i];
				Array[i] = Array[j];
				Array[j] = Temp;
			}
		}
		for (i = 0; i < Count; i++)printf("%d ", Array[i]);
		printf("\n");
	}
	return 0;
}