#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node_t {
    char Opera;
    int Num;
    struct node_t *Prev, *Next;
} node;

node *CreateNode(char Opera, int Num, node *Prev, node *Next) {
    node *Node = (node *) malloc(sizeof(node));
    Node->Opera = Opera;
    Node->Num = Num;
    Node->Prev = Prev;
    if (Prev) Prev->Next = Node;
    Node->Next = Next;
    if (Next) Next->Prev = Node;
    return Node;
}

node *ProcessNode(node *Node) {
    while (Node && Node->Prev) Node = Node->Prev;
    while (Node && Node->Next) {
        Node = Node->Next;
        if (Node->Opera == '*' || Node->Opera == '/' || Node->Opera == '%') {
            int Num = 0;
            if (Node->Opera == '*') Num = Node->Prev->Num * Node->Next->Num;
            else if (Node->Opera == '/') Num = Node->Prev->Num / Node->Next->Num;
            else if (Node->Opera == '%') Num = Node->Prev->Num % Node->Next->Num;
            node *PrevTemp = Node->Prev, *NextTemp = Node->Next;
            Node = CreateNode('\0', Num, Node->Prev->Prev, Node->Next->Next);
            free(PrevTemp);
            free(NextTemp);
        }
    }
    while (Node && Node->Prev) Node = Node->Prev;
    while (Node && Node->Next) {
        Node = Node->Next;
        if (Node->Opera == '+' || Node->Opera == '-') {
            int Num = 0;
            if (Node->Opera == '+') Num = Node->Prev->Num + Node->Next->Num;
            else if (Node->Opera == '-') Num = Node->Prev->Num - Node->Next->Num;
            node *PrevTemp = Node->Prev, *NextTemp = Node->Next;
            Node = CreateNode('\0', Num, Node->Prev->Prev, Node->Next->Next);
            free(PrevTemp);
            free(NextTemp);
        }
    }
    return Node;
}

int main() {
    while (1) {
        char String[1024] = "", *Result = NULL;
        while ((Result = gets(String)) && Result) {
            node *Node = NULL;
            char *Value = strtok(String, " ");
            while (Value) {
                if (Value[0] == '+' || Value[0] == '-' || Value[0] == '*' || Value[0] == '/' || Value[0] == '%')
                    Node = CreateNode(Value[0], 0, Node, NULL);
                else Node = CreateNode('\0', atoi(Value), Node, NULL);
                Value = strtok(NULL, " ");
            }
            Node = ProcessNode(Node);
            if (Node) {
                printf("%d", Node->Num);
                free(Node);
            }
            printf("\n");
        }
        if (!Result) break;
    }
    return 0;
}