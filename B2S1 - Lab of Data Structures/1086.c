#include <stdio.h>

void Hanoi(int *Count, int Num, char Char1, char Char2, char Char3) {
    if (Num == 1) printf("%2d. Move disk %d from %c to %c\n", ++(*Count), Num, Char1, Char3);
    else {
        Hanoi(Count, Num-1, Char1, Char3, Char2);
        printf("%2d. Move disk %d from %c to %c\n", ++(*Count), Num, Char1, Char3);
        Hanoi(Count, Num-1, Char2, Char1, Char3);
    }
}

int main() {
    int Num = 0, Count = 0;
    while (scanf("%d", &Num) != EOF) {
        Count = 0;
        Hanoi(&Count, Num, 'X', 'Y', 'Z');
        printf("\n");
    }
    return 0;
}