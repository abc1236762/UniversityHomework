#define swap(x, y) ((x) ^= (y)), ((y) ^= (x)), ((x) ^= (y))

#define arr_swap(arr, i, j) if ((i) != (j)) ((arr)[i] ^= (arr)[j]), ((arr)[j] ^= (arr)[i]), ((arr)[i] ^= (arr)[j])

void sel_sort(int *arr, int len) {
	for (int i = 0; i < len - 1; i++) {
		int min_i = i;
		for (int j = i + 1; j < len; j++) if (arr[j] < arr[min_i]) min_i = j;
		arr_swap(arr, i , min_i);
	}
}

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

int arr_bin_search(const int *arr, int len, int key) {
	int first = 0, last = len - 1, mid = (first + last) / 2;
	while (first <= last) {
		if (arr[mid] < key) first = mid + 1;
		else if (arr[mid] > key) last = mid - 1;
		else return mid;
		mid = (first + last) / 2;
	}
	return -1;
}
