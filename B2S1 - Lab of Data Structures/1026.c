#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct node_t {
	int ID;
	struct node_t *Next;
} node;

typedef struct point_t {
	node *Node;
	bool IsWalked;
} point;

node *CreateNode(int ID, node *Prev, node *Next) {
	node *Node = (node *) malloc(sizeof(node));
	Node->ID = ID;
	Node->Next = Next;
	if (Prev) Prev->Next = Node;
	return Node;
}

node *MakeGraph(node *Node, int Point) {
	node *Search = Node;
	while (Search && Search->Next && Search->Next->ID < Point) Search = Search->Next;
	Search ? CreateNode(Point, Search, Search->Next) : (Node = CreateNode(Point, NULL, NULL));
	return Node;
}

void WalkGraph(point **Graph, point *Point) {
	(*(Graph + Point->Node->ID - 1))->IsWalked = true;
	printf("%d ", Point->Node->ID);
	node *Node = Point->Node;
	while (Node) {
		if ((*(Graph + Node->ID - 1))->IsWalked) Node = Node->Next;
		else WalkGraph(Graph, *(Graph + Node->ID - 1));
	}
}

void FreeGraph(point **Graph, int Vertex) {
	int i = 0;
	for (i = 0; i < Vertex; i++) {
		node *Temp = NULL;
		while ((*(Graph + i))->Node) {
			Temp = (*(Graph + i))->Node;
			(*(Graph + i))->Node = (*(Graph + i))->Node->Next;
			free(Temp);
		}
		free(*(Graph + i));
	}
	free(Graph);
}

int main() {
	point **Graph = NULL;
	int Vertex = 0, Edge = 0, i = 0;
	while (scanf("%d%d", &Vertex, &Edge) != EOF) {
		Graph = (point **) malloc(sizeof(point *) * Vertex);
		for (i = 0; i < Vertex; i++) {
			*(Graph + i) = (point *) malloc(sizeof(point));
			(*(Graph + i))->Node = MakeGraph(NULL, i + 1);
			(*(Graph + i))->IsWalked = false;
		}
		for (i = 0; i < Edge; i++) {
			int PointA = 0, PointB = 0;
			scanf("%d%d", &PointA, &PointB);
			(*(Graph + PointA - 1))->Node = MakeGraph((*(Graph + PointA - 1))->Node, PointB);
			(*(Graph + PointB - 1))->Node = MakeGraph((*(Graph + PointB - 1))->Node, PointA);
		}
		WalkGraph(Graph, *Graph);
		printf("\n");
		FreeGraph(Graph, Vertex);
	}
	return 0;
}