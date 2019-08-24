#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct _node {
	struct _node *Next;
} node;

node *StackAdd(node *Node) {
	node *NewNode = (node *) malloc(sizeof(node));
	NewNode->Next = NULL;
	while (Node && Node->Next) Node = Node->Next;
	Node ? (Node->Next = NewNode) : (Node = NewNode);
	return Node;
}

bool StackPop(node **Node) {
	if (!(*Node)) return false;
	while ((*Node)->Next && (*Node)->Next->Next) *Node = (*Node)->Next;
	if ((*Node)->Next) {
		free((*Node)->Next);
		(*Node)->Next = NULL;
	} else {
		free(*Node);
		*Node = NULL;
	}
	return true;
}

int main() {
	int Group = 0, Input = 0, Count = 0;
	node *Node = NULL;
	while (scanf("%d", &Group) != EOF && getchar()) {
		while (Group--) {
			Count = 0;
			while ((Input = getchar()) && Input != EOF && Input != (int) '\n') {
				if (Input == (int) 'B') Node = StackAdd(Node);
				else if (Input == (int) 'G') if (StackPop(&Node)) Count++;
			}
			printf("%d\n", Count);
			while (Node) StackPop(&Node);
		}
	}
	return 0;
}