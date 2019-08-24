#include <stdio.h>
#include <stdbool.h>

int main() {
	int Count = 0, Line = 0;
	while (scanf("%d%d", &Count, &Line) != EOF) {
		int ParentNodes[Line], ChildNodes[Line], TopNodes[Count], TopNodesCount = 0, i = 0, j = 0;
		for (i = 0; i < Line; i++) scanf("%d%d", ParentNodes + i, ChildNodes +i);
		for (i = 0; i < Line; i++) {
			bool IsTopNode = true, Included = false;
			for (j = 0; j < Line; j++) if (ParentNodes[i] == ChildNodes[j]) IsTopNode = false;
			if (!IsTopNode) continue;
			for (j = 0; j < TopNodesCount; j++) if (ParentNodes[i] == TopNodes[j]) Included = true;
			if (!Included) TopNodes[TopNodesCount++] = ParentNodes[i];
		}
		printf("%d\n", TopNodesCount);
		for (i = 0; i < TopNodesCount; i++) printf("%d ", TopNodes[i]);
		printf("\n");
	}
	return 0;
}