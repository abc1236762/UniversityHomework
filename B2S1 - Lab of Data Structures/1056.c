#include <stdio.h>
#include <stdlib.h>

typedef struct node_t {
    int Value;
    struct node_t *Prior, *Next;
} node;

node *SearchList(node *First, int Index) {
    if (!First || Index < -1) return NULL;
    if (Index == 0) return First;
    if (Index == -1) return First->Prior;
    node *Node = First->Next;
    while (Node != First && --Index) Node = Node->Next;
    if (Node == First && 0 < Index) return NULL;
    else return Node;
}

void PrintList(node *First) {
    if (First) {
        node *Node = First;
        printf("%d", Node->Value);
        while (Node->Next != First) {
            Node = Node->Next;
            printf(" %d", Node->Value);
        }
    }
    printf("\n");
}

node *CreateNode(node *First, int Index, int Value) {
    node *SearchNode = SearchList(First, Index - 1), *Node = NULL;
    if (SearchNode || !Index) {
        Node = (node *) malloc(sizeof(node));
        Node->Value = Value;
        if (SearchNode) {
            Node->Prior = SearchNode;
            Node->Next = SearchNode->Next;
            SearchNode->Next = SearchNode->Next->Prior = Node;
        } else Node->Next = Node->Prior = Node;
    }
    return (Index != 0 && First) ? First : Node;
}

node *DeleteNode(node *First, int Index) {
    node *SearchNode = SearchList(First, Index);
    if (SearchNode) {
        if (First == SearchNode) First = First->Next;
        SearchNode->Prior->Next = SearchNode->Next;
        SearchNode->Next->Prior = SearchNode->Prior;
        free(SearchNode);
    }
    return First;
}

int main() {
    int Function = 0, Index = 0, Value = 0;
    node *First = NULL;
    while (scanf("%d", &Function) != EOF) {
        if (Function == 0) PrintList(First);
        else if (Function == 1) {
            scanf("%d%d", &Index, &Value);
            First = CreateNode(First, Index - 1, Value);
        } else if (Function == 2) {
            scanf("%d", &Index);
            First = DeleteNode(First, Index - 1);
        }
    }
    return 0;
}