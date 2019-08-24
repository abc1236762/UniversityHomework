#include <stdio.h>
#include <string.h>
#define STR_MAX 1000

void DictSort(char Array[STR_MAX][STR_MAX], int Size) {
	int i = 0, j = 0, k = 0;
	for (i = 0; i < Size - 1; i++) for (j = i + 1; j < Size; j++) if (strcmp(Array[i], Array[j]) > 0) {
		char Temp[STR_MAX];
		strcpy(Temp, Array[i]);
		strcpy(Array[i], Array[j]);
		strcpy(Array[j], Temp);
	}
}

int main() {
	char String[STR_MAX] = "", Table[STR_MAX][STR_MAX];
	while (scanf("%s", String) != EOF) {
		int i = 0;
		for (i = 0; i < strlen(String); i++) strcpy(Table[i], String+i);
		DictSort(Table, (int) strlen(String));
		for (i = 0; i < strlen(String); i++) printf("%s\n", Table[i]);
	}
	return 0;
}