#include <stdio.h>

int Find(int Map[20][20], int Width, int Height, int i, int j) {
    if (((i >= Height || i < 0) || (j >= Width || j < 0)) || Map[i][j] == (int) '#') return 0;
    Map[i][j] = (int) '#';
    return Find(Map, Width, Height, i - 1, j) +
           Find(Map, Width, Height, i + 1, j) +
           Find(Map, Width, Height, i, j - 1) +
           Find(Map, Width, Height, i, j + 1) + 1;
}

int main() {
    int Map[20][20] = {{0}}, Width = 0, Height = 0, i = 0, j = 0;
    while (scanf("%d%d", &Width, &Height) != EOF) {
        getchar();
        if (!Width && !Height) break;
        for (i = 0; i < Height; i++) {
            for (j = 0; j < Width; j++)
                Map[i][j] = getchar();
            getchar();
        }
        for (i = 0; i < Height; i++) {
            for (j = 0; j < Width; j++) {
                if (Map[i][j] == (int) '@') {
                    printf("%d\n", Find(Map, Width, Height, i, j));
                    break;
                }
            }
        }
    }
    return 0;
}