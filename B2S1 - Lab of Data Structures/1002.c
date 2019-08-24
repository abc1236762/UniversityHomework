#include <stdio.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char ID[512];
    char Name[512];
    char Sex[512];
    unsigned short Age;
} Student;

int main() {
    while (1) {
        unsigned short StudentCount = 0, SearchCount = 0, i = 0, j = 0;
        if (scanf("%hu", &StudentCount) == EOF) break;
        Student Students[StudentCount];
        for (i = 0; i < StudentCount; i++) {
            scanf("%s%s%s%hu", Students[i].ID, Students[i].Name, Students[i].Sex, &(Students[i].Age));
        }
        scanf("%hu", &SearchCount);
        for (i = 0; i < SearchCount; i++) {
            char SearchID[512] = {'\0'};
            bool IsFounded = false;
            scanf("%s", SearchID);
            for (j = 0; j < StudentCount; j++) {
                if (!strcmp(SearchID, Students[j].ID)) {
                    IsFounded = true;
                    break;
                }
            }
            if (IsFounded)
                printf("%s %s %s %d\n", Students[j].ID, Students[j].Name, Students[j].Sex, Students[j].Age);
            else printf("No Answer!\n");
        }
    }
    return 0;
}