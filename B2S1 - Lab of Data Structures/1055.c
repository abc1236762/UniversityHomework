#include <stdio.h>
#include <stdlib.h>

typedef struct node_t {
    int Num;
    struct node_t *Prev;
    struct node_t *Next;
} node;

node *CreateNode(int Num, node *Prev, node *Next) {
    node *Node = (node *) malloc(sizeof(node));
    Node->Num = Num;
    Node->Prev = Prev;
    if (Prev) Prev->Next = Node;
    Node->Next = Next;
    if (Next) Next->Prev = Node;
    return Node;
}

void InsertNode(node *Node, int Num) {
    while (Node) {
        if (Node->Num >= Num) {
            if (Node->Prev && Node->Prev->Num >= Num) {
                Node = Node->Prev;
                continue;
            } else {
                CreateNode(Num, Node->Prev, Node);
                break;
            }
        } else {
            if (Node->Next && Node->Next->Num <= Num) {
                Node = Node->Next;
                continue;
            } else {
                CreateNode(Num, Node, Node->Next);
                break;
            }
        }
    }
}

void PrintAndFreeNode(node *Node) {
    while (Node && Node->Prev) Node = Node->Prev;
    while (Node) {
        node *NodeTemp = Node;
        printf("%d", Node->Num);
        if (Node->Next) printf(" ");
        Node = Node->Next;
        free(NodeTemp);
    }
    printf("\n");
}

int main() {
    int First = 0, Second = 0, i = 0;
    while (scanf("%d", &First) != EOF) {
        int Num = 0;
        node *Node = NULL;
        for (i = 0; i < First; i++) {
            scanf("%d", &Num);
            Node = CreateNode(Num, Node, NULL);
        }
        scanf("%d", &Second);
        for (i = 0; i < Second; i++) {
            scanf("%d", &Num);
            InsertNode(Node, Num);
        }
        PrintAndFreeNode(Node);
    }
    return 0;
}