#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct _magic {
	char Name[21], Effect[81];
	int Index;
	struct _magic *Next;
} magic;

void GetMagic(const char Temp[104], char Name[21], char Effect[81]) {
	int i = 0;
	for (i = 0; i < 104; i++) if (Temp[i] == ']') break;
	memset(Name, '\0', 21);
	memcpy(Name, &Temp[1], (size_t) (i - 1));
	memset(Effect, '\0', 81);
	memcpy(Effect, &Temp[i + 2], strlen(Temp) - i - 2);
}

magic *AddToTable(magic *Magic, const char Name[21], const char Effect[81], const int *Index) {
	magic *Last = Magic, *Now = NULL;
	while (Last && Last->Next) Last = Last->Next;
	Now = (magic *) malloc(sizeof(magic));
	memcpy(Now->Name, &Name[0], 21);
	memcpy(Now->Effect, &Effect[0], 81);
	Now->Index = *Index;
	Now->Next = NULL;
	Last ? (Last->Next = Now) : (Last = Now);
	return Magic ? Magic : Last;
}

magic *GetEffect(magic *Table[128][128], const char Name[21]) {
	magic *Selected = NULL;
	int i = 0;
	for (i = 0; i < 128; i++) {
		magic *Now = Table[Name[0]][i];
		while (Now) {
			if (strcmp(Now->Name, Name) == 0 && (!Selected || Now->Index < Selected->Index)) Selected = Now;
			Now = Now->Next;
		}
	}
	return Selected;
}

magic *GetName(magic *Table[128][128], const char Effect[81]) {
	magic *Selected = NULL;
	int i = 0;
	for (i = 0; i < 128; i++) {
		magic *Now = Table[i][Effect[0]];
		while (Now) {
			if (strcmp(Now->Effect, Effect) == 0 && (!Selected || Now->Index < Selected->Index)) Selected =  Now;
			Now = Now->Next;
		}
	}
	return Selected;
}

int main() {
	char Temp[104], Name[21], Effect[81];
	int i = 0, Count = 0;
	magic *Table[128][128] = {{NULL}};
	while (1) {
		memset(Temp, '\0', 104);
		if (gets(Temp) && strcmp(Temp, "@END@") == 0) break;
		GetMagic(Temp, Name, Effect);
		Table[Name[0]][Effect[0]] = AddToTable(Table[Name[0]][Effect[0]], Name, Effect, &i);
		i++;
	}
	scanf("%d", &Count);
	getchar();
	for (i = 0; i < Count; i++) {
		magic *Now = NULL;
		gets(Temp);
		if (Temp[0] == '[') {
			memset(Name, '\0', 21);
			memcpy(Name, &Temp[1], strlen(Temp) - 2);
			Now = GetEffect(Table, Name);
			if (Now) printf("%s\n", Now->Effect);
		} else {
			memset(Effect, '\0', 81);
			memcpy(Effect, &Temp[0], strlen(Temp));
			Now = GetName(Table, Effect);
			if (Now) printf("%s\n", Now->Name);
		}
		if (!Now) printf("what?\n");
	}
	return 0;
}