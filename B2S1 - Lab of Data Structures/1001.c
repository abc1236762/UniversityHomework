#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct term_t {
	int Coefficient, Degree;
} term;

term **GetPolynomial() {
	char String[200] = {'\0'}, *Temp;
	int i = 0, j = 0;
	if (!gets(String) || !strlen(String)) return NULL;
	term **Polynomial = (term **) malloc(sizeof(term *) * 100);
	for (i = 0; i < 100; i++) *(Polynomial + i) = NULL;
	i = 0;
	Temp = strtok(String, " ");
	while (Temp) {
		if (j++ % 2) (*(Polynomial + i++))->Degree = atoi(Temp);
		else {
			*(Polynomial + i) = (term *) malloc(sizeof(term));
			(*(Polynomial + i))->Coefficient = atoi(Temp);
		}
		Temp = strtok(NULL, " ");
	}
	return Polynomial;
}

void PolynomialAdd(term **PolynomialA, term **PolynomialB) {
	int i = -1;
	while (*(PolynomialB + ++i)) {
		int j = -1;
		while (*(PolynomialA + ++j)) if ((*(PolynomialB + i))->Degree == (*(PolynomialA + j))->Degree) break;
		if (!*(PolynomialA + j)) {
			*(PolynomialA + j) = (term *) malloc(sizeof(term));
			(*(PolynomialA + j))->Coefficient = 0;
			(*(PolynomialA + j))->Degree = (*(PolynomialB + i))->Degree;
		}
		(*(PolynomialA + j))->Coefficient += (*(PolynomialB + i))->Coefficient;
	}
}

void PrintPolynomial(term **Polynomial) {
	int i = -1;
	while (*(Polynomial + ++i)) {
		int j = -1;
		while (*(Polynomial + ++j + 1)) {
			if ((*(Polynomial + j))->Degree < (*(Polynomial + j + 1))->Degree) {
				term *Temp = *(Polynomial + j);
				*(Polynomial + j) = *(Polynomial + j + 1);
				*(Polynomial + j + 1) = Temp;
			}
		}
	}
	i = -1;
	while (*(Polynomial + ++i)) {
		if (!(*(Polynomial + i))->Coefficient) continue;
		printf("%d %d", (*(Polynomial + i))->Coefficient, (*(Polynomial + i))->Degree);
		if (*(Polynomial + i + 1)) printf(" ");
	}
	printf("\n");
}

void FreePolynomial(term **Polynomial) {
	int i = -1;
	while (*(Polynomial + ++i)) free(*(Polynomial + i));
	free(Polynomial);
}

int main() {
	term **PolynomialA = NULL, **PolynomialB = NULL;
	while ((PolynomialA = GetPolynomial()) && PolynomialA) {
		PolynomialB = GetPolynomial();
		PolynomialAdd(PolynomialA, PolynomialB);
		PrintPolynomial(PolynomialA);
		FreePolynomial(PolynomialA);
		FreePolynomial(PolynomialB);
	}
	return 0;
}