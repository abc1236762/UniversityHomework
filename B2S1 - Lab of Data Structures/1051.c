#include <stdio.h>
 
typedef struct {
    int ID;
    char Name[20];
    unsigned char Point[3];
} Student;
 
int main() {
    Student Students[10];
    unsigned short TotalPoint[3] = { 0 };
    unsigned char MaximumPointStudent = 0;
    unsigned char i = 0;
     
    for (i = 0; i < 10; i++) {
        scanf("%d%s%hhu%hhu%hhu", &Students[i].ID, Students[i].Name,
            &Students[i].Point[0], &Students[i].Point[1], &Students[i].Point[2]);
        TotalPoint[0] += Students[i].Point[0];
        TotalPoint[1] += Students[i].Point[1];
        TotalPoint[2] += Students[i].Point[2];
        if (((Students[i].Point[0] + Students[i].Point[1] + Students[i].Point[2]) / 3.0)
            >= ((Students[MaximumPointStudent].Point[0] + Students[MaximumPointStudent].Point[1]
            + Students[MaximumPointStudent].Point[2]) / 3.0)) { MaximumPointStudent = i; }
    }
     
    printf("%.2f %.2f %.2f\n", TotalPoint[0] / 10.0, TotalPoint[1] / 10.0, TotalPoint[2] / 10.0);
    printf("%d %s %hhu %hhu %hhu\n", Students[MaximumPointStudent].ID,
        Students[MaximumPointStudent].Name, Students[MaximumPointStudent].Point[0],
        Students[MaximumPointStudent].Point[1], Students[MaximumPointStudent].Point[2]);
}