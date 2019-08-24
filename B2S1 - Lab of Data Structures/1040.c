#include <stdio.h>
#include <stdbool.h>
#include <memory.h>

typedef struct _table {
	int Key;
	char Name[128];
} table;

int main() {
	while (1) {
		int i = 0;
		bool IsEOF = false;
		table Table[26];
		for (i = 0; i < 26; i++) Table[i].Key = -1;
		for (i = 0; i < 26; i++) {
			char Name[128];
			IsEOF = scanf("%s", Name) == EOF;
			if (IsEOF) break;
			int Index = Name[0] - 'A';
			while (1) {
				if (Table[Index].Key >= 0) Index = (Index + 1) % 26;
				else break;
			}
			memcpy(Table[Index].Name, Name, 128);
			Table[Index].Key = Table[Index].Name[0] - 'A';
		}
		if (IsEOF) break;
		for (i = 0; i < 26; i++) printf("%d %d %s\n", i, Table[i].Key, Table[i].Name);
	}
	return 0;
}