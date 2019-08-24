#include <stdio.h>
#include <stdlib.h>

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

int main(int argc, char *argv[]) {
	int n = 0, r = 0;
	scanf("%d", &n);
	while (n--) {
		scanf("%d", &r);
		int s[r], result = 0;
		for (int i = 0; i < r; i++) scanf("%d", &s[i]);
		mrg_sort(s, 0, r - 1);
		for (int i = 0; i < r; i++) result += abs(s[r / 2] - s[i]);
		printf("%d\n", result);
	}
	return 0;
}