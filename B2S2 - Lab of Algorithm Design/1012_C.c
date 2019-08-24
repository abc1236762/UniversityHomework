#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void mrg_sort(int *arr, int first, int last) {
	if (first < last) {
		int mid = (first + last) / 2;
		mrg_sort(arr, first, mid);
		mrg_sort(arr, mid + 1, last);
		int left_len = mid - first + 1, right_len = last - mid, left[left_len], right[right_len];
		for (int i = 0; i < left_len; i++) left[i] = arr[first + i];
		for (int i = 0; i < right_len; i++) right[i] = arr[mid + 1 + i];
		int left_i = 0, right_i = 0, arr_i = first;
		while (left_i < left_len && right_i < right_len) {
			if (left[left_i] <= right[right_i]) arr[arr_i] = left[left_i++];
			else arr[arr_i] = right[right_i++];
			arr_i++;
		}
		while (left_i < left_len) arr[arr_i++] = left[left_i++];
		while (right_i < right_len) arr[arr_i++] = right[right_i++];
	}
}

int arr_bin_search(const int *arr, int len, int key, bool is_bigger) {
	int first = 0, last = len - 1, mid = (first + last) / 2, index = -1;
	while (first <= last) {
		if (arr[mid] < key) first = mid + 1;
		else if (arr[mid] > key) last = mid - 1;
		else {
			index = mid;
			break;
		}
		mid = (first + last) / 2;
	}
	if (arr[mid] != key) index = is_bigger ? last : first;
	if (is_bigger) while (index < len - 1 && arr[index] == arr[index + 1]) index++;
	else while (index > 0 && arr[index] == arr[index - 1]) index--;
	return index;
}

int main(int argc, char *argv[]) {
	int n = 0, m = 0;
	while (scanf("%d%d", &n, &m) != EOF && n > 0 && m > 0) {
		int *data = (int *)malloc(sizeof(int) * n), min = 0, max = 0;
		for (int i = 0; i < n; i++) scanf("%d", data + i);
		mrg_sort(data, 0, n - 1);
		while (m--) {
			scanf("%d%d", &min, &max);
			printf("%d\n", arr_bin_search(data, n, max, true) - arr_bin_search(data, n, min, false) + 1);
		}
		free(data);
	}
	return 0;
}