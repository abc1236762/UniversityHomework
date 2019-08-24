#include <stdio.h>
#include <stdbool.h>

bool Check(int Array[100][100], int Size) {
	int i = 0, j = 0, Temp1 = 0, Temp2 = 0;
	for (i = 0; i < Size; i++) {
		Temp1 = Temp2 = 0;
		for (j = 0; j < Size; j++) {
			Temp1 += Array[i][j];
			Temp2 += Array[j][i];
		}
		if (Temp1 % 2 || Temp2 % 2) return false;
	}
	return true;
}

int main() {
	int Array[100][100] = {{0}}, Size = 0, i = 0, j = 0;
	while (scanf("%d", &Size) != EOF && Size) {
		for (i = 0; i < Size; i++)
			for (j = 0; j < Size; j++)
				scanf("%d", &Array[i][j]);
		if (Check(Array, Size)) printf("OK\n");
		else {
			bool IsOK = false;
			for (i = 0; i < Size; i++) {
				for (j = 0; j < Size; j++) {
					Array[i][j] = !Array[i][j];
					if ((IsOK = Check(Array, Size)) && IsOK) {
						printf("Change bit (%d,%d)\n", i + 1, j + 1);
						break;
					}
					Array[i][j] = !Array[i][j];
				}
				if (IsOK) break;
			}
			if (!IsOK) printf("Corrupt\n");
		}
	}
	return 0;
}