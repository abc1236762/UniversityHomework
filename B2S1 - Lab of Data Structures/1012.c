#include <stdio.h>
#include <stdlib.h>

typedef struct node_t {
    int ID;
    int Num;
    struct node_t *Left, *Right;
} node;

node *MakeTree(node *Node, int ID, int Num) {
    if (!Node) {
        Node = (node *) malloc(sizeof(node));
        Node->ID = ID;
        Node->Num = Num;
        Node->Left = Node->Right = NULL;
    } else {
        if (Node->Num > Num) Node->Left = MakeTree(Node->Left, ID, Num);
        else Node->Right = MakeTree(Node->Right, ID, Num);
    }
    return Node;
}

void PrintTreeMid(node *Node) {
    if (!Node) return;
    PrintTreeMid(Node->Left);
    printf("%d %d\n", Node->ID, Node->Num);
    PrintTreeMid(Node->Right);
}

int main() {
    int ID = 0, Num = 0, Length = 0, i = 0;
    while (scanf("%d", &Length) != EOF) {
        node *Node = NULL;
        for (i = 0; i < Length; i++) {
            scanf("%d%d", &ID, &Num);
            Node = MakeTree(Node, ID, Num);
        }
        PrintTreeMid(Node);
    }
    return 0;
}
