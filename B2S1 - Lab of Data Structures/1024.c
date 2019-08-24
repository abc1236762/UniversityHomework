#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct _node {
	int Value;
	int Cost;
	struct _node *Next;
} node;

typedef struct {
	node *Line;
	bool IsWalked;
} point;

typedef struct {
	point **Points;
	int PointCount;
} map;

node *CreateNode(int Value, int Cost, node *Prev, node *Next) {
	node *Node = (node *) malloc(sizeof(node));
	Node->Value = Value;
	Node->Cost = Cost;
	Node->Next = Next;
	if (Prev) Prev->Next = Node;
	return Node;
}

node *AddPoint(node *Node, int Value, int Cost) {
	node *Prev = NULL, *Next = Node;
	while (Next && Next->Cost < Cost) {
		Prev = Next;
		Next = Next->Next;
	}
	Prev ? CreateNode(Value, Cost, Prev, Next) : (Node = CreateNode(Value, Cost, Prev, Next));
	return Node;
}

map *MakeMap(int PointCount) {
	int i = 0;
	map *Map = (map *) malloc(sizeof(map));
	Map->Points = (point **) malloc(sizeof(point *) * PointCount);
	for (i = 0; i < PointCount; i++) {
		*(Map->Points + i) = (point *) malloc(sizeof(point));
		(*(Map->Points + i))->Line = NULL;
		(*(Map->Points + i))->IsWalked = false;
	}
	Map->PointCount = PointCount;
}

void FreeMap(map *Map) {
	int i = 0;
	for (i = 0; i < Map->PointCount; i++) {
		node *Node = (*(Map->Points + i))->Line, *Temp = NULL;
		while (Node) {
			Temp = Node;
			Node = Node->Next;
			free(Temp);
		}
		free(*(Map->Points + i));
	}
	free(Map->Points);
	free(Map);
}

int FindResult(map *Map, int StartPoint) {
	int i = 0, Point = StartPoint, Result = 0, MinCost = 0;
	while (Point >= 0) {
		(*(Map->Points + Point))->IsWalked = true;
		Result += MinCost;
		MinCost = Point = -1;
		for (i = 0; i < Map->PointCount; i++) {
			if ((*(Map->Points + i))->IsWalked) {
				node *Node = (*(Map->Points + i))->Line;
				while (Node) {
					if ((MinCost < 0 || MinCost > Node->Cost) && !(*(Map->Points + Node->Value))->IsWalked) {
						Point = Node->Value;
						MinCost = Node->Cost;
						break;
					}
					Node = Node->Next;
				}
			}
		}
	}
	return Result;
}

int main() {
	int Group = 0;
	map *Map = NULL;
	while (scanf("%d", &Group) != EOF) {
		while (Group--) {
			int PointCount = 0, LineCount = 0, i = 0;
			scanf("%d%d", &PointCount, &LineCount);
			Map = MakeMap(PointCount);
			for (i = 0; i < LineCount; i++) {
				int PointA = 0, PointB = 0, Cost = 0;
				scanf("%d%d%d", &PointA, &PointB, &Cost);
				(*(Map->Points + PointA))->Line = AddPoint((*(Map->Points + PointA))->Line, PointB, Cost);
				(*(Map->Points + PointB))->Line = AddPoint((*(Map->Points + PointB))->Line, PointA, Cost);
			}
			printf("%d\n", FindResult(Map, 0));
			FreeMap(Map);
		}
	}
	return 0;
}