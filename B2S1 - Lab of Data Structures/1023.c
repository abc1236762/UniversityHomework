#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int FindMinDistance(int **Map, int Cities, int From, int To) {
	int Distance[Cities];
	bool Found[Cities];
	for (int i = 0; i < Cities; i++) {
		Distance[i] = Map[From][i];
		Found[i] = false;
	}
	Found[From] = true;
	Distance[From] = 0;
	for (int i = 1; i < Cities; i++) {
		int IndexOfMin = -1;
		for (int j = 0; j < Cities; j++) {
			if (Found[j] || Distance[j] < 0) continue;
			if (IndexOfMin < 0 || Distance[j] < Distance[IndexOfMin]) IndexOfMin = j;
		}
		if (IndexOfMin < 0) continue;
		else if (IndexOfMin == To) break;
		Found[IndexOfMin] = true;
		for (int j = 0; j < Cities; j++) {
			if (Found[j] || Map[IndexOfMin][j] < 0) continue;
			if (Distance[j] < 0 || Distance[IndexOfMin] + Map[IndexOfMin][j] < Distance[j]) {
				Distance[j] = Distance[IndexOfMin] + Map[IndexOfMin][j];
			}
		}
	}
	return Distance[To];
}

int main() {
	int Cities = 0, Lines = 0;
	while (scanf("%d%d", &Cities, &Lines) != EOF) {
		int **Map = (int **)malloc(sizeof(int *) * Cities), CityA = 0, CityB = 0, MinDistance = 0;
		for (int i = 0; i < Cities; i++) {
			Map[i] = (int *)malloc(sizeof(int) * Cities);
			for (int j = 0; j < Cities; j++) Map[i][j] = -1;
		}
		for (int i = 0; i < Lines; i++) {
			int Distance = 0;
			scanf("%d%d%d", &CityA, &CityB, &Distance);
			Map[CityA - 1][CityB - 1] = Map[CityB - 1][CityA - 1] = Distance;
		}
		scanf("%d%d", &CityA, &CityB);
		MinDistance = FindMinDistance(Map, Cities, CityA - 1, CityB - 1);
		if (MinDistance > 0) printf("%d\n", MinDistance);
		else printf("No path\n");
	}
	return 0;
}