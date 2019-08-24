#include <stdio.h>
#include <stdlib.h>

void MergeSort(int *Array, int Size, int Start, int End, int *SwapTime) {
	if (Start < End) {
		int Mid = (Start + End) / 2;
		MergeSort(Array, Size, Start, Mid, SwapTime);
		MergeSort(Array, Size, Mid + 1, End, SwapTime);
		int i = 0, j = 0, Start1 = Start, Start2 = Mid + 1;
		int *SortedArray = (int *) malloc(sizeof(int) * (End - Start + 1));
		for (i = 0; Start1 <= Mid && Start2 <= End; i++) {
			if (Array[Start1] <= Array[Start2]) {
				SortedArray[i] = Array[Start1];
				Start1++;
			} else {
				*SwapTime += Mid - Start1 + 1;
				SortedArray[i] = Array[Start2];
				Start2++;
			}
		}
		for (; Start1 <= Mid; i++, Start1++) SortedArray[i] = Array[Start1];
		for (; Start2 <= End; i++, Start2++) SortedArray[i] = Array[Start2];
		for (i = 0, j = Start; i <= End - Start; i++, j++) Array[j] = SortedArray[i];
		free(SortedArray);
	}
}

int main() {
	int Size = 0;
	while (scanf("%d", &Size) != EOF) {
		if (Size == 0) break;
		int i = 0, SwapTime = 0, *Array = (int *) malloc(sizeof(int) * Size);
		for (i = 0; i < Size; i++) scanf("%d", Array + i);
		MergeSort(Array, Size, 0, Size - 1, &SwapTime);
		printf("%d\n", SwapTime);
		free(Array);
	}
	return 0;
}