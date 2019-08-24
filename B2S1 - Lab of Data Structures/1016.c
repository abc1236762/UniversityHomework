
#include <stdio.h>
#include <stdlib.h>

typedef struct _point {
	int X, Y, Step;
	struct _point *Next;
} point;

point *MakePoint(int X, int Y, int Step) {
	point *Point = (point *) malloc(sizeof(point));
	Point->X = X;
	Point->Y = Y;
	Point->Step = Step;
	Point->Next = NULL;
	return Point;
}

int SearchMap(char **Map, int Width, int Height, int X, int Y) {
	int i, NextX, NextY;
	int Direction[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
	point *Point = MakePoint(X, Y, 0), *Next = MakePoint(-1, -1, -1);
	Point->Next = Next;
	while (Point != Next) {
		for (i = 0; i < 4; i++) {
			NextX = Point->X + Direction[i][0];
			NextY = Point->Y + Direction[i][1];
			if (NextX >= 0 && NextX < Width && NextY >= 0 && NextY < Height && Map[NextY][NextX] != '#') {
				if (Map[NextY][NextX] == 'E') return Point->Step + 1;
				Map[NextY][NextX] = '#';
				Next->X = NextX;
				Next->Y = NextY;
				Next->Step = Point->Step + 1;
				Next->Next = MakePoint(-1, -1, -1);
				Next = Next->Next;
			}
		}
		Point = Point->Next;
	}
	return -1;
}

int main() {
	int Group = 0;
	scanf("%d", &Group);
		int Width = 0, Height = 0, StartX = -1, StartY = -1, i = 0, j = 0, k = 0;
		for (i = 0; i < Group; i++) {
			scanf("%d%d", &Height, &Width);
			getchar();
			char **Map = (char **) malloc(sizeof(char *) * Height);
			for (j = 0; j < Height; j++) {
				Map[j] = (char *) malloc(sizeof(char) * Width);
				for (k = 0; k < Width; k++) {
					Map[j][k] = (char) getchar();
					if (Map[j][k] == 'S') {
						StartX = k;
						StartY = j;
					}
				}
				getchar();
			}
			printf("%d\n", SearchMap(Map, Width, Height, StartX, StartY));
		}
	return 0;
}