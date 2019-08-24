#include <stdio.h>

int main() {
    while (1) {
        char input[16][16] = {{'\0'}};
        int i = 0, j = 0;
        for (i = 0; i < 16; i++) {
            for (j = 0; j < 16; j++) {
                scanf("%c", &(input[i][j]));
                if (input[i][j] == ' ' || input[i][j] == '\n') {
                    break;
                }
            }
            if (input[i][j] == '\n') {
                input[i][j] = '\0';
                break;
            }
        }
        if (input[0][0] == ' ' && input[1][0] == ' ') break;

        for (i = 0; i < 16; i++) {
            for (j = 0; j < 16; j++) {
                if (j == 0) {
                    if (input[i][j] >= 'a' && input[i][j] <= 'z') input[i][j] -= 32;
                } else {
                    if (input[i][j] >= 'A' && input[i][j] <= 'Z') input[i][j] += 32;
                }
                if (input[i][j] != ' ' && input[i][j] != '\0') printf("%c", input[i][j]);
            }
        }
        printf("\n");
    }
    printf("over");
    return 0;
}