#include <stdio.h>

int main() {
    int Count = 0, Person = 0, i = 0;
    while (scanf("%d", &Count) != EOF) {
        int WindowA[1001] = {0}, WindowB[2001] = {0}, CountA = 0, CountB = 0;
        for (i = 0; i < Count; i++) {
            scanf("%d", &Person);
            if (Person % 2) WindowA[CountA++] = Person;
            else WindowB[CountB++] = WindowB[CountB++] = Person;
        }
        for (i = 0; i < CountA || i < CountB; i++) {
            if (i < CountA && WindowA[i] != WindowA[i + 1]) {
                if (i > 0) printf(" ");
                printf("%d", WindowA[i]);
            }
            if (i < CountB && WindowB[i] != WindowB[i + 1]) {
                if (i > 1 || (i - 1 < CountA && WindowA[i - 1] != WindowA[i])) printf(" ");
                printf("%d", WindowB[i]);
            }
        }
        printf("\n");
    }
    return 0;
}