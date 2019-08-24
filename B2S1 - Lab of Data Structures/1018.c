#include <stdio.h>
#include <stdlib.h>

typedef struct node_t {
    int Num;
    struct node_t *Left, *Right;
} node;

node *MakeTree(node *Node, int Num) {
    if (!Node) {
        Node = (node *) malloc(sizeof(node));
        Node->Num = Num;
        Node->Left = Node->Right = NULL;
    } else {
        if (Node->Num > Num) Node->Left = MakeTree(Node->Left, Num);
        else Node->Right = MakeTree(Node->Right, Num);
    }
    return Node;
}

void PrintTreeMid(node *Node) {
    if (!Node) return;
    PrintTreeMid(Node->Left);
    printf("%d ", Node->Num);
    PrintTreeMid(Node->Right);
}

void PrintTreeBack(node *Node) {
    if (!Node) return;
    PrintTreeBack(Node->Left);
    PrintTreeBack(Node->Right);
    printf("%d ", Node->Num);
}

int main() {
    int Num = 0, Length = 0, i = 0;
    while (scanf("%d", &Length) != EOF) {
        node *Node = NULL;
        for (i = 0; i < Length; i++) {
            scanf("%d", &Num);
            Node = MakeTree(Node, Num);
        }
        PrintTreeMid(Node);
        printf("\n");
        PrintTreeBack(Node);
        printf("\n");
    }
    return 0;
}
