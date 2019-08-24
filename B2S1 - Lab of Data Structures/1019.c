#include <stdio.h>
#include <stdlib.h>

typedef struct _node {
	char Value;
	struct _node *Parent, *Left, *Right;
} node;

void PreOrder(node *Node) {
	if (!Node) return;
	printf("%c", Node->Value);
	PreOrder(Node->Left);
	PreOrder(Node->Right);
}

void InOrder(node *Node) {
	if (!Node) return;
	InOrder(Node->Left);
	printf("%c", Node->Value);
	InOrder(Node->Right);
}

void PostOrder(node *Node) {
	if (!Node) return;
	PostOrder(Node->Left);
	PostOrder(Node->Right);
	printf("%c", Node->Value);
}

int main() {
	int Count = 0, i = 0;
	while (scanf("%d", &Count) != EOF) {
		node *Tree[Count], *Head = NULL;
		for (i = 0; i < Count; i++) {
			Tree[i] = (node *) malloc(sizeof(node));
			Tree[i]->Parent = NULL;
		}
		for (i = 0; i < Count; i++) {
			getchar();
			int LeftIndex = 0, RightIndex = 0;
			scanf("%c%d%d", &(Tree[i]->Value), &LeftIndex, &RightIndex);
			if (LeftIndex) {
				Tree[i]->Left = Tree[LeftIndex - 1];
				Tree[LeftIndex - 1]->Parent = Tree[i];
			} else Tree[i]->Left = NULL;
			if (RightIndex) {
				Tree[i]->Right = Tree[RightIndex - 1];
				Tree[RightIndex - 1]->Parent = Tree[i];
			} else Tree[i]->Right = NULL;
		}
		for (i = 0; i < Count; i++) if (!Tree[i]->Parent) Head = Tree[i];
		PreOrder(Head);
		printf("\n");
		InOrder(Head);
		printf("\n");
		PostOrder(Head);
		printf("\n");
	}
	return 0;
}