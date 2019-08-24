#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool is_bicolored(int **graph, int *color, int nodes, int lines, int index) {
	bool judge = true;
	for (int i = 0; i < lines && graph[index][i] >= 0; i++) {
		if (color[graph[index][i]] != 0 && color[graph[index][i]] == color[index]) return false;
		if (color[graph[index][i]] == 0) {
			color[graph[index][i]] = (color[index] == 1 ? 2 : 1);
			judge &= is_bicolored(graph, color, nodes, lines, graph[index][i]);
		}
	}
	return judge;
}

int main(int argc, char *argv[]) {
	int n = 0, l = 0;
	while (scanf("%d", &n) != EOF && n > 0) {
		int **graph = (int **)malloc(sizeof(int *) * n), color[n];
		scanf("%d", &l);
		for (int i = 0; i < n; i++) {
			graph[i] = (int *)malloc(sizeof(int) * l);
			for (int j = 0; j < l; j++) graph[i][j] = -1;
		}
		for (int i = 0; i < l; i++) {
			int a = 0, b = 0;
			scanf("%d%d", &a, &b);
			for (int j = 0; j < l; j++) if (graph[a][j] < 0) {
				graph[a][j] = b;
				break;
			}
			for (int j = 0; j < l; j++) if (graph[b][j] < 0) {
				graph[b][j] = a;
				break;
			}
		}
		for (int i = 0; i < n; i++) color[i] = 0;
		color[0] = 1;
		printf(is_bicolored(graph, color, n, l, 0) ? "BICOLORABLE.\n" : "NOT BICOLORABLE.\n");
		free(graph);
	}
	return 0;
}