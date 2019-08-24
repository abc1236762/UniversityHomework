#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int ID;
    int Score[5];
} Student;

bool IsStudentFail(Student *StudentsPtr);
bool IsStudentAbove(Student *StudentsPtr);

int main() {
    Student Students[4];
    Student *StudentsPtr = Students;
    while (1) {
        int i = 0, j = 0, Score1Total = 0;
        bool End = false;
        for (i = 0; i < 4; i++) {
            if (scanf("%d%d%d%d%d%d", &(StudentsPtr + i)->ID,
                      &(StudentsPtr + i)->Score[0],
                      &(StudentsPtr + i)->Score[1],
                      &(StudentsPtr + i)->Score[2],
                      &(StudentsPtr + i)->Score[3],
                      &(StudentsPtr + i)->Score[4]) == EOF) {
                End = true;
                break;
            }
            Score1Total += (StudentsPtr + i)->Score[0];
        }
        if (End) break;
        printf("%.2lf\n", Score1Total / 4.0);
        for (i = 0; i < 4; i++) {
            if (IsStudentFail(StudentsPtr + i)) {
                int ScoreTotal = 0;
                for (j = 0; j < 5; j++) {
                    ScoreTotal += (StudentsPtr + i)->Score[j];
                }
                printf("%d %d %d %d %d %d %.2lf\n",
                       (StudentsPtr + i)->ID,
                       (StudentsPtr + i)->Score[0],
                       (StudentsPtr + i)->Score[1],
                       (StudentsPtr + i)->Score[2],
                       (StudentsPtr + i)->Score[3],
                       (StudentsPtr + i)->Score[4],
                       ScoreTotal / 5.0);
            }
        }
        for (i = 0; i < 4; i++) {
            if (IsStudentAbove(StudentsPtr + i))
                printf("%d ", (StudentsPtr + i)->ID);
        }
        printf("\n");
    }
    return 0;
}

bool IsStudentFail(Student *StudentPtr) {
    int Fail = 0, j= 0;
    for (j = 0; j < 5; j++) {
        if (StudentPtr->Score[j] < 60) Fail += 1;
    }
    if (Fail >= 2) return true;
    return false;
}

bool IsStudentAbove(Student *StudentPtr){
    int ScoreTotal = 0, Pass = 0, j= 0;
    for (j = 0; j < 5; j++) {
        ScoreTotal += StudentPtr->Score[j];
        if (StudentPtr->Score[j] >= 85) Pass += 1;
    }
    if (Pass == 5 || ScoreTotal >= 90 * 5) return true;
    return false;
}