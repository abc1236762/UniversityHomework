#include <stdio.h>

int main() {
	int Count = 0, i = 0, j = 0, k = 0, l = 0, m = 0, n = 0;
	while (scanf("%d", &Count) != EOF && Count > 0) {
		int Array[Count];
		for (i = 0; i < Count; i++) scanf("%d", Array + i);
		for (i = 0; i < Count - 5; i++)
			for (j = i + 1; j < Count - 4; j++)
				for (k = j + 1; k < Count - 3; k++)
					for (l = k + 1; l < Count - 2; l++)
						for (m = l + 1; m < Count - 1; m++)
							for (n = m + 1; n < Count; n++)
								printf("%d %d %d %d %d %d\n", Array[i], Array[j], Array[k], Array[l], Array[m], Array[n]);
		printf("\n");
	}
	return 0;
}