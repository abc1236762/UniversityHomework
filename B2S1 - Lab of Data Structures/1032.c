#include <stdio.h>
#include <stdbool.h>


void Swap(char *Char1, char *Char2) {
	char Temp = *Char1;
	*Char1 = *Char2;
	*Char2 = Temp;
}

void Reverse(char *String, int From, int To) {
	for (int i = From; i <= (To + From) / 2; i++)
		Swap(&String[i], &String[To - (i - From)]);
}

bool NextPermutation(char *String, int Length, int *Count) {
	int Last = Length - 2;
	while (Last >= 0 && String[Last] >= String[Last + 1]) Last--;
	if (Last < 0) return false;
	int Select = Length - 1;
	while (String[Select] <= String[Last]) Select--;
	Swap(&String[Last], &String[Select]);
	Reverse(String, Last + 1, Length - 1);
	(*Count)++;
	return true;
}

void Sort(char *String, int Length) {
	for (int i = 0; i < Length - 1; i++) for (int j = 0; j < Length - 1 - i; j++)
		if (String[j] > String[j + 1]) Swap(&String[j], &String[j + 1]);
}

int main() {
	int Length = 0;
	while (scanf("%d", &Length) != EOF) {
		getchar();
		int Count = Length ? 1 : 0;
		char String[Length + 1];
		scanf("%s", String);
		Sort(String, Length);
		printf("%s\n", String);
		while (NextPermutation(String, Length, &Count)) printf("%s\n", String);
		printf("%d\n", Count);
	}
	return 0;
}