#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

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

void StackAdd(stack *Stack, int Value) {
	if (GetStackTop(Stack) != Stack->Top) {
		node *Node = Stack->Node, *NewNode = (node *) malloc(sizeof(node));
		NewNode->Value = Value;
		NewNode->Next = NULL;
		while (Node && Node->Next) Node = Node->Next;
		Node ? (Node->Next = NewNode) : (Stack->Node = NewNode);
	}
}

int StackPop(stack *Stack) {
	int Value = -1;
	if (GetStackTop(Stack)) {
		node *Node = Stack->Node;
		while (Node->Next && Node->Next->Next) Node = Node->Next;
		if (Node->Next) {
			Value = Node->Next->Value;
			free(Node->Next);
			Node->Next = NULL;
		} else {
			Value = Stack->Node->Value;
			free(Stack->Node);
			Stack->Node = NULL;
		}
	}
	return Value;
}

void FreeStackNode(stack *Stack) {
	node *Node = Stack->Node;
	while (Node) {
		node *Temp = Node;
		Node = Node->Next;
		free(Temp);
	}
	Stack->Node = NULL;
}

int main() {
	stack *Stack = (stack *) malloc(sizeof(stack));
	Stack->Top = 15;
	Stack->Node = NULL;
	while (true) {
		int Value = 0;
		bool IsError = false;
		while ((Value = getchar()) && Value != (int) '\n' && Value != EOF) {
			if (Value == (int) '+' || Value == (int) '-' || Value == (int) '*' || Value == (int) '/') {
				int Value1 = StackPop(Stack), Value2 = StackPop(Stack);
				if (Value1 < 0 || Value2 < 0) IsError = true;
				else {
					if (Value == (int) '+') Value = Value2 + Value1;
					else if (Value == (int) '-') Value = Value2 - Value1;
					else if (Value == (int) '*') Value = Value2 * Value1;
					else Value = Value2 / Value1;
					StackAdd(Stack, Value);
				}
			} else if (Value >= (int) '0' && Value <= (int) '9') StackAdd(Stack, Value - (int) '0');
			else IsError = true;
		}
		IsError || GetStackTop(Stack) > 1 ? printf("Input Error\n") : printf("%d\n", StackPop(Stack));
		FreeStackNode(Stack);
		if (Value == EOF) break;
	}
	return 0;
}