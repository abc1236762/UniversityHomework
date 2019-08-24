#include <stdio.h>
#include <stdlib.h>

typedef struct {
	int Row, Col, Value;
} element;

typedef struct {
	int Row, Col, Count;
	element *Elements;
} matrix;

void AddElement(matrix *Matrix, int Row, int Col, int Value) {
	int i = 0;
	element *OldElements = Matrix->Elements;
	Matrix->Count++;
	Matrix->Elements = (element *) malloc(sizeof(element) * Matrix->Count);
	for (i = 0; i < Matrix->Count - 1; i++) Matrix->Elements[i] = OldElements[i];
	Matrix->Elements[i].Row = Row;
	Matrix->Elements[i].Col = Col;
	Matrix->Elements[i].Value = Value;
	if (OldElements) free(OldElements);
}

void Transpose(matrix *Matrix) {
	int Temp = Matrix->Row, i = 0;
	Matrix->Row = Matrix->Col;
	Matrix->Col = Temp;
	for (i = 0; i < Matrix->Count; i++) {
		Temp = Matrix->Elements[i].Row;
		Matrix->Elements[i].Row = Matrix->Elements[i].Col;
		Matrix->Elements[i].Col = Temp;
	}
}

int main() {
	int Row = 0, Col = 0, Value = 0, i = 0, j = 0, k = 0;
	while (scanf("%d%d", &Row, &Col) != EOF) {
		matrix *Matrix = (matrix *) malloc(sizeof(matrix));
		Matrix->Row = Row;
		Matrix->Col = Col;
		Matrix->Count = 0;
		Matrix->Elements = NULL;
		for (i = 0; i < Matrix->Row; i++) for (j = 0; j < Matrix->Col; j++) if (scanf("%d", &Value) && Value) AddElement(Matrix, i, j, Value);
		Transpose(Matrix);
		for (i = 0; i < Matrix->Row; i++) {
			for (j = 0; j < Matrix->Col; j++) {
				Value = 0;
				for (k = 0; k < Matrix->Count; k++) if (Matrix->Elements[k].Row == i && Matrix->Elements[k].Col == j) Value = Matrix->Elements[k].Value;
				printf("%d", Value);
				if (j != Matrix->Col - 1) printf(" ");
			}
			printf("\n");
		}
		free(Matrix->Elements);
		free(Matrix);
	}
	return 0;
}