#include <stdio.h>
#include <stdbool.h>

int FindMinDistance(int **Map, int Places, int From, int To) {
	int Distance[Places];
	bool Found[Places];
	for (int i = 0; i < Places; i++) {
		Distance[i] = Map[From][i];
		Found[i] = false;
	}
	Found[From] = true;
	Distance[From] = 0;
	for (int i = 1; i < Places; i++) {
		int IndexOfMin = -1;
		for (int j = 0; j < Places; j++) {
			if (Found[j] || Distance[j] < 0) continue;
			if (IndexOfMin < 0 || Distance[j] < Distance[IndexOfMin]) IndexOfMin = j;
		}
		if (IndexOfMin < 0) continue;
		else if (IndexOfMin == To) break;
		Found[IndexOfMin] = true;
		for (int j = 0; j < Places; j++) {
			if (Found[j] || Map[IndexOfMin][j] < 0) continue;
			if (Distance[j] < 0 || Distance[IndexOfMin] + Map[IndexOfMin][j] < Distance[j]) {
				Distance[j] = Distance[IndexOfMin] + Map[IndexOfMin][j];
			}
		}
	}
	return Distance[To];
}

int main() {
	int Places = 0, Lines = 0;
	while (scanf("%d%d", &Places, &Lines) != EOF) {
		if (!Places && !Lines) break;
		int Map[Places][Places], *MapPointer[Places], PlaceA = 0, PlaceB = 0;
		for (int i = 0; i < Places; i++) {
			MapPointer[i] = Map[i];
			for (int j = 0; j < Places; j++) Map[i][j] = -1;
		}
		for (int i = 0; i < Lines; i++) {
			int Distance = 0;
			scanf("%d%d%d", &PlaceA, &PlaceB, &Distance);
			if (Map[PlaceA - 1][PlaceB - 1] < 0 || Distance < Map[PlaceA - 1][PlaceB - 1])
				Map[PlaceA - 1][PlaceB - 1] = Map[PlaceB - 1][PlaceA - 1] = Distance;
		}
		printf("%d\n", FindMinDistance(MapPointer, Places, 0, Places - 1));
	}
	return 0;
}