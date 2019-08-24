#include <stdio.h>
#include <stdlib.h>

typedef struct word {
    char Char;
    struct word *Previous;
} line;

line *AddWordChar(char Char, line *Previous) {
    line *Line = (line *) malloc(sizeof(line));
    Line->Char = Char;
    Line->Previous = Previous;
    return Line;
}

int main() {
    int LineCount = 0, i = 0;
    while (scanf("%d", &LineCount) != EOF && getchar() == '\n') {
        for (i = 0; i < LineCount; i++) {
            line *Line = NULL;
            char Char = '\0', Output[1000] = {'\0'};
            int OutputCount = 0, CharResult = 0;
            while (Char != '\n' && CharResult != EOF) {
                CharResult = scanf("%c", &Char);
                if (Char == ' ' || Char == '\n' || CharResult == EOF) {
                    while (Line) {
                        line *LineTemp = Line;
                        Output[OutputCount++] = Line->Char;
                        Line = Line->Previous;
                        free(LineTemp);
                    }
                    if (Char == ' ') Output[OutputCount++] = ' ';
                } else Line = Line ? AddWordChar(Char, Line) : AddWordChar(Char, NULL);
            }
            printf("%s\n", Output);
            free(Line);
        }
    }
    return 0;
}