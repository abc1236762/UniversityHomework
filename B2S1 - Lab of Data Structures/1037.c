#include <stdio.h>
#include <stdlib.h>

void Sort(int *Array, int Size) {
	int i = 0, j = 0;
	for (i = 0; i < Size - 1; i++) {
		for (j = 1; j < Size; j++) {
			if (Array[j] < Array[i]) {
				int Temp = Array[i];
				Array[i] = Array[j];
				Array[j] = Temp;
			}
		}
	}
}

int IndexOf(const int *Array, int Value) {
	int i = 0;
	for (i = 0; i < sizeof(Array); i++) {
		if (Array[i] == Value) return i;
	}
	return -1;
}

int main() {
	int Groups = 0;
	while (scanf("%d", &Groups) != EOF) {
		int i = 0;
		for (i = 0; i < Groups; i++) {
			int CustomerCount = 0, Position = 0, Distance = 0, j = 0;
			scanf("%d", &CustomerCount);
			int Customers[CustomerCount], SortedCustomers[CustomerCount];
			for (j = 0; j < CustomerCount; j++) scanf("%d", Customers + j);
			for (j = 0; j < CustomerCount; j++)SortedCustomers[j] = Customers[j];
			Sort(SortedCustomers, CustomerCount);
			if (CustomerCount % 2) Position = SortedCustomers[CustomerCount / 2];
			else {
				Position = IndexOf(Customers, SortedCustomers[CustomerCount / 2 - 1]) <
					IndexOf(Customers, SortedCustomers[CustomerCount / 2]) ?
					SortedCustomers[CustomerCount / 2 - 1] : SortedCustomers[CustomerCount / 2];
			}
			for (j = 0; j < CustomerCount; j++) Distance += abs(Customers[j] - Position);
			printf("%d %d\n", Position, Distance);
		}
	}
	return 0;
}