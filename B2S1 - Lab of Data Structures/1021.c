#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct _node {
	char Value;
	struct _node *Child, *Next;
} node;

node *CreateNode(char Value) {
	node *Node = (node *)malloc(sizeof(node));
	Node->Value = Value;
	Node->Next = Node->Child = NULL;
	return Node;
}

void MakeTree(node **Tree, char *String, int *NodeCount) {
	node *Node = (*Tree)->Child, *Parent = *Tree;
	int i = 0;
	for (i = 0; i < strlen(String); i++) {
		while (Node && Node->Next) {
			if (Node->Value == String[i]) break;
			Node = Node->Next;
		}
		if (Node) {
			if (Node->Value == String[i]) Parent = Node;
			else {
				Parent = Node->Next = CreateNode(String[i]);
				(*NodeCount)++;
			}
		} else {
			Parent = Parent->Child = CreateNode(String[i]);
			(*NodeCount)++;
		}
		Node = Parent->Child;
	}
}

int main() {
	int NodeCount = 1;
	char String[64] = "";
	node *Head = CreateNode('\0');
	while (scanf("%s", String)!=EOF) MakeTree(&Head, String, &NodeCount);
	printf("%d", NodeCount);
	return 0;
}