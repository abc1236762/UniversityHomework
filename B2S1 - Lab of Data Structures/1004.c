#include <stdio.h>

int main() {
	int Count = 0, Array[50] = {0}, ID = 0, i = 0;
	while (scanf("%d", &Count) && Count) {
		printf("Set #%d\n", ++ID);
		int Sum = 0, Time = 0;
		for (i = 0; i < Count; i++) {
			scanf("%d", &Array[i]);
			Sum += Array[i];
		}
		for (i = 0; i < Count; i++) if (Sum / Count - Array[i] > 0) Time += Sum / Count - Array[i];
		printf("The minimum number of moves is %d.\n\n", Time);
	}
	return 0;
}