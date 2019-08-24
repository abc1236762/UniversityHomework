#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct _node {
	int X, Y;
	struct _node *Next;
} node;

typedef struct _queue {
	int Max;
	node *Node;
} queue;

queue *MakeQueue(int Max) {
	queue *Queue = (queue *) malloc(sizeof(queue));
	Queue->Max = Max;
	Queue->Node = NULL;
	return Queue;
}

bool QueuePushNode(queue *Queue, int X, int Y) {
	int Count = 1;
	node *Node = Queue->Node, *Temp;
	while (Node && Node->Next) {
		Node = Node->Next;
		Count++;
	}
	if (Count == Queue->Max) return false;
	Temp = (node *) malloc(sizeof(node));
	Temp->X = X;
	Temp->Y = Y;
	Temp->Next = NULL;
	Node ? (Node->Next = Temp) : (Queue->Node = Temp);
	return true;
}

bool QueuePopNode(queue *Queue) {
	if (!Queue->Node)return false;
	node *Temp = Queue->Node;
	Queue->Node = Queue->Node->Next;
	free(Temp);
	return true;
}

bool QueueCheckSameNodeValue(queue *Queue, int X, int Y) {
	node *Node = Queue->Node;
	while (Node) {
		if (Node->X == X && Node->Y == Y) return true;
		Node = Node->Next;
	}
	return false;
}

int main() {
	queue *Queue = MakeQueue(20);
	int Count = 0, Temp = 0;
	while (scanf("%d", &Count) != EOF && Count > 0) {
		getchar();
		int X = 0, Y = 0, i = 0;
		for (X = 11, Y = 25; X <= 30 && Y <= 25; X++) QueuePushNode(Queue, X, Y);
		X--;
		bool IsFailed = false;
		for (i = 0; i < Count; i++) {
			Temp = getchar();
			if (!IsFailed) {
				if (Temp == (int) 'N') Y--;
				else if (Temp == (int) 'S') Y++;
				else if (Temp == (int) 'W') X--;
				else if (Temp == (int) 'E') X++;
				QueuePopNode(Queue);
				if (X > 50 || X <= 0 || Y > 50 || Y <= 0) {
					printf("The worm ran off the board on move %d.\n", i + 1);
					IsFailed = true;
				} else if (QueueCheckSameNodeValue(Queue, X, Y)) {
					printf("The worm ran into itself on move %d.\n", i + 1);
					IsFailed = true;
				}
				QueuePushNode(Queue, X, Y);
			}
		}
		if (!IsFailed) printf("The worm successfully made all %d moves.\n", Count);
		while (QueuePopNode(Queue)) {}
		getchar();
	}
	return 0;
}