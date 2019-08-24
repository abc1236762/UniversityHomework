#include <stdio.h>

int main() {
    int Line = 0, i = 0;
    while (scanf("%d", &Line) != EOF) {
        char String[5] = {'\0'};
        scanf("%s", String);
        for (i = 0; i < 2; i++) {
            char Temp = String[i];
            String[i] = String[4 - 1 - i];
            String[4 - 1 - i] = Temp;
        }
        printf("%s\n", String);
    }
    return 0;
}
