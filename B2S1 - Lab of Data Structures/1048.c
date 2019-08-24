#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct _node {
	char Color;
	struct _node *Nodes[4];
} node;

node *CreateNode(char Color) {
	node *Node = (node *)malloc(sizeof(node));
	Node->Color = Color;
	for (int i = 0; i < 4; i++) Node->Nodes[i] = NULL;
	return Node;
}

char CheckColor(char **Image, int StartX, int StartY, int Length) {
	bool IsSame = true;
	char Color = Image[StartY][StartX];
	for (int i = 0; i < Length; i++) for (int j = 0; j < Length; j++)
		if (Image[StartY + i][StartX + j] != Color) IsSame = false;
	return IsSame ? Color : (char)'g';
}

void MakeTree(node **Tree, char **Image, int Length, int StartX, int StartY, int *Count) {
	char Color = CheckColor(Image, StartX, StartY, Length);
	*Tree = CreateNode(Color);
	(*Count)++;
	if (Length > 1 && Color == 'g') {
		Length /= 2;
		MakeTree(&((*Tree)->Nodes[0]), Image, Length, StartX + Length, StartY, Count);
		MakeTree(&((*Tree)->Nodes[1]), Image, Length, StartX, StartY, Count);
		MakeTree(&((*Tree)->Nodes[2]), Image, Length, StartX, StartY + Length, Count);
		MakeTree(&((*Tree)->Nodes[3]), Image, Length, StartX + Length, StartY + Length, Count);
	}
}

void DFSTrace(const node *Node, int *Index, int Count) {
	if (!Node) return;
	printf("%c", Node->Color);
	++(*Index) < Count ? printf(" ") : printf("\n");
	for (int i = 0; i < 4; i++) DFSTrace(Node->Nodes[i], Index, Count);
}


int main() {
	int Length = 0;
	while (scanf("%d", &Length) != EOF) {
		int Count = 0, Index = 0;
		char Image[Length][Length], *ImagePointer[Length];
		node *Root = NULL;
		for (int i = 0; i < Length; i++) {
			getchar();
			for (int j = 0; j < Length; j++) Image[i][j] = getchar() == '1' ? (char)'b' : (char)'w';
			ImagePointer[i] = Image[i];
		}
		MakeTree(&Root, ImagePointer, Length, 0, 0, &Count);
		DFSTrace(Root, &Index, Count);
	}
	return 0;
}