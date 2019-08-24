#include <stdio.h>
#include <stdbool.h>

void PairColors(int **Graph, int Points, int Colors, int Point, int *Color, int *Count) {
	if (Point == Points) (*Count)++;
	else {
		for (int i = 0; i < Colors; i++) {
			Color[Point] = i;
			bool Paired = true;
			for (int j = 0; j < Points; j++) if (Graph[Point][j] == 1 && Color[Point] == Color[j]) Paired = false;
			if (Paired) PairColors(Graph, Points, Colors, Point + 1, Color, Count);
			Color[Point] = -1;
		}
	}
}

int main() {
	int Points = 0, Lines = 0, Colors = 0;
	scanf("%d%d%d", &Points, &Lines, &Colors);
		int Graph[Points][Points], *GraphPointer[Points], Color[Points], Count = 0;
		for (int i = 0; i < Points; i++) {
			GraphPointer[i] = Graph[i];
			for (int j = 0; j < Points; j++) Graph[i][j] = 0;
			Color[i] = -1;
		}
		for (int i = 0; i < Lines; i++) {
			int PointA = 0, PointB = 0;
			scanf("%d%d", &PointA, &PointB);
			Graph[PointA - 1][PointB - 1] = Graph[PointB - 1][PointA - 1] = 1;
		}
		PairColors(GraphPointer, Points, Colors, 0, Color, &Count);
		printf("%d\n", Count);
	return 0;
}