#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct node_t {
    bool Switch;
    struct node_t *Left, *Right;
} node;

node *CreateTree(int Depth) {
    if (Depth == 0) return NULL;
    node *Node = (node *) malloc(sizeof(node));
    Node->Switch = false;
    Node->Left = CreateTree(Depth - 1);
    Node->Right = CreateTree(Depth - 1);
    return Node;
}

int Monkey(node *Node) {
    int ID = 1;
    while (Node && (Node->Left || Node->Right)) {
        Node->Switch = !Node->Switch;
        if (!Node->Switch) {
            Node = Node->Right;
            ID += ID + 1;
        } else {
            Node = Node->Left;
            ID += ID;
        }
    }
    return ID;
}

int main() {
    int Depth = 0, MonkeyCount = 0, Location = 0, i = 0;
    while (scanf("%d%d", &Depth, &MonkeyCount) != EOF) {
        if (!Depth && !MonkeyCount) break;
        node *Tree = CreateTree(Depth);
        for (i = 0; i < MonkeyCount; i++) Location = Monkey(Tree);
        printf("%d\n", Location);
    }
    return 0;
}