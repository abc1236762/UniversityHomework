#include <stdio.h>
#include <stdlib.h>

typedef struct _node {
	int Value;
	int Children;
	struct _node **ChildNodes;
} node;

void FindNode(node *Node, int Value, node **FoundNode) {
	int i = 0;
	if (!Node) return;
	if (Node->Value == Value) *FoundNode = Node;
	else for (i = 0; i < Node->Children; i++) FindNode(Node->ChildNodes[i], Value, FoundNode);
}

node *CreateNode(int Value) {
	node *Node = (node *) malloc(sizeof(node));
	Node->Value = Value;
	Node->Children = 0;
	Node->ChildNodes = NULL;
	return Node;
}

void MakeTree(node **Tree, int ParentValue, int ChildValue) {
	node *Parent = NULL, *Child = NULL;
	FindNode(*Tree, ParentValue, &Parent);
	FindNode(*Tree, ChildValue, &Child);
	if (!Parent) Parent = CreateNode(ParentValue);
	if (!Child) Child = CreateNode(ChildValue);
	node **ChildNodes = (node **) malloc(sizeof(node *) * Parent->Children + 1);
	int i = 0;
	for (i = 0; i < Parent->Children; i++) ChildNodes[i] = Parent->ChildNodes[i];
	ChildNodes[Parent->Children++] = Child;
	Parent->ChildNodes = ChildNodes;
	if (!*Tree || *Tree == Child) *Tree = Parent;
}


void MaxChildren(node *Node, node **MaxChildNode) {
	if (!Node) return;
	int i = 0;
	if (!*MaxChildNode) *MaxChildNode = Node;
	for (i = 0; i < Node->Children; i++) {
		if (Node->ChildNodes[i]->Children > (*MaxChildNode)->Children ||
			(Node->ChildNodes[i]->Children == (*MaxChildNode)->Children &&
			Node->ChildNodes[i]->Value > (*MaxChildNode)->Value)) *MaxChildNode = Node->ChildNodes[i];
		MaxChildren(Node->ChildNodes[i], MaxChildNode);
	}
}

int main() {
	int Nodes = 0, Lines = 0, ParentValue, ChildValue, i = 0;
	while (scanf("%d%d", &Nodes, &Lines) != EOF) {
		node *Tree = NULL, *MaxChildNode = NULL;
		for (i = 0; i < Lines; i++) {
			scanf("%d%d", &ParentValue, &ChildValue);
			MakeTree(&Tree, ParentValue, ChildValue);
		}
		MaxChildren(Tree, &MaxChildNode);
		printf("%d\n%d\n",Tree->Value, MaxChildNode->Value);
		for (i = 0; i < MaxChildNode->Children; i++) printf("%d ", MaxChildNode->ChildNodes[i]->Value);
		printf("\n");
	}
	return 0;
}