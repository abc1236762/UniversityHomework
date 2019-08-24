#include <stdio.h>
#include <stdbool.h>

int main() {
    int Size = 0, i = 0, j = 0;
    while (scanf("%d", &Size) != EOF) {
        int Data[Size][Size];
        for (i = 0; i < Size; i++) {
            for (j = 0; j < Size; j++) {
                scanf("%d", &Data[i][j]);
            }
        }
        bool IsTrue = true;
        for (i = 0; i < Size; i++) {
            for (j = 0; j <= i; j++) {
                if (Data[i][j] != Data[j][i]) IsTrue = false;
            }
        }
        IsTrue ? printf("Yes!\n") : printf("No!\n");
    }
    return 0;
}
