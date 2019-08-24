#include <stdio.h>
#include <stdlib.h>

typedef struct node_t {
	int Value;
	struct node_t *Next;
} node;

typedef struct {
	int Top;
	node *Node;
} stack;

int GetStackTop(stack *Stack) {
	int Top = 0;
	node *Node = Stack->Node;
	while (Node) {
		Node = Node->Next;
		Top++;
	}
	return Top;
}

void PrintStack(stack *Stack) {
	node *Node = Stack->Node;
	while (Node) {
		printf("%d", Node->Value);
		Node = Node->Next;
		if (Node) printf(" ");
	}
	printf("\n");
}

void StackAdd(stack *Stack, int Value) {
	if (GetStackTop(Stack) == Stack->Top) printf("Stack Full\n");
	else {
		node *Node = Stack->Node, *NewNode = (node *) malloc(sizeof(node));
		NewNode->Value = Value;
		NewNode->Next = NULL;
		while (Node && Node->Next) Node = Node->Next;
		Node ? (Node->Next = NewNode) : (Stack->Node = NewNode);
		PrintStack(Stack);
	}
}

void StackPop(stack *Stack) {
	if (!GetStackTop(Stack)) printf("Stack Empty\n");
	else {
		node *Node = Stack->Node;
		while (Node->Next && Node->Next->Next) Node = Node->Next;
		if (Node->Next) {
			free(Node->Next);
			Node->Next = NULL;
			PrintStack(Stack);
		} else {
			free(Stack->Node);
			Stack->Node = NULL;
			printf("Stack Empty\n");
		}
	}
}

int main() {
	int Func = 0, Value = 0;
	stack *Stack = (stack*)malloc(sizeof(stack));
	Stack->Top = 4;
	Stack->Node = NULL;
	while (scanf("%d", &Func) != EOF) {
		if (Func == 1 && scanf("%d", &Value) != EOF) StackAdd(Stack, Value);
		else if (Func == 2) StackPop(Stack);
	}
	return 0;
}