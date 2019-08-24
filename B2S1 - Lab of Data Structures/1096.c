#include <stdio.h>
#include <stdlib.h>

typedef struct heap_t {
    int *Data, Size;
} heap;


void SwapValue(int *Value1, int *Value2) {
    int Temp = *Value1;
    *Value1 = *Value2;
    *Value2 = Temp;
}

heap *CreateHeap(heap *Heap, int Size) {
    Heap = (heap *) malloc(sizeof(heap));
    Heap->Size = Size;
    Heap->Data = (int *) malloc(sizeof(int) * Size);
    return Heap;
}

void MaxHeap(heap *Heap, int Index) {
    if (!Heap) return;
    while (Index + 1 <= Heap->Size / 2)
        if (Heap->Data[Index] < Heap->Data[(Index + 1) * 2 - 1] || Heap->Data[Index] < Heap->Data[(Index + 1) * 2]) {
            if (Heap->Data[(Index + 1) * 2 - 1] >= Heap->Data[(Index + 1) * 2]) {
                SwapValue(&Heap->Data[Index], &Heap->Data[(Index + 1) * 2 - 1]);
                Index = (Index + 1) * 2 - 1;
            } else {
                SwapValue(&Heap->Data[Index], &Heap->Data[(Index + 1) * 2]);
                Index = (Index + 1) * 2;
            }
        } else break;
}

void PrintAndFreeHeap(heap *Heap) {
    if (!Heap) return;
    int i = 0;
    for (i = 0; i < Heap->Size; i++) {
        printf("%d", Heap->Data[i]);
        if (i < Heap->Size - 1) printf(" ");
    }
    free(Heap->Data);
    free(Heap);
    printf("\n");
}

int main() {
    int Size = 0, Value = 0, i = 0;
    heap *Heap = NULL;
    while (scanf("%d", &Size) != EOF) {
        Heap = CreateHeap(Heap, Size);
        for (i = 0; i < Size; i++) {
            scanf("%d", &Value);
            Heap->Data[i] = Value;
        }
        for (i = Size; i > 0; i--) MaxHeap(Heap, i - 1);
        PrintAndFreeHeap(Heap);
    }
    return 0;
}