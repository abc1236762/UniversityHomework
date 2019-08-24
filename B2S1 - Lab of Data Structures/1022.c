#include <stdio.h>
#include <stdlib.h>

typedef struct node_t {
    char Char;
    struct node_t *Left, *Right;
} node;

int IndexOf(const char *Array, int Start, int End, char Char) {
    while (Start <= End) if (Array[Start++] == Char) return Start - 1;
}

node *MakeTree(node *Tree, int ArrayLength,
               const char *InArray, int InStart, int InEnd,
               const char *PostArray, int PostStart, int PostEnd) {
    if (InStart > InEnd || PostStart > PostEnd) return NULL;
    Tree = (node *) malloc(sizeof(node));
    Tree->Left = Tree->Right = NULL;
    Tree->Char = PostArray[PostEnd];
    int Index = IndexOf(InArray, InStart, InEnd, Tree->Char),
            LeftCount = Index - InStart, RightCount = InEnd - Index;
    if (LeftCount > 0)
        Tree->Left = MakeTree(Tree->Left, ArrayLength,
                              InArray, InStart, InStart + LeftCount - 1,
                              PostArray, PostStart, PostStart + LeftCount - 1);
    if (RightCount > 0)
        Tree->Right = MakeTree(Tree->Right, ArrayLength,
                               InArray, InEnd - RightCount + 1, InEnd,
                               PostArray, PostEnd - RightCount, PostEnd - 1);
    return Tree;
}

void PrintPreOrder(node *Tree) {
    if (Tree) {
        printf("%c", Tree->Char);
        PrintPreOrder(Tree->Left);
        PrintPreOrder(Tree->Right);
    }
}

int main() {
    int Length = 0, CharInt = 0;
    char InArray[27] = {'\0'}, PostArray[27] = {'\0'};
    Length = 0;
    while ((CharInt = getchar()) && (char) CharInt != '\n' && CharInt != EOF) {
        InArray[Length++] = (char) CharInt;
    }
    Length = 0;
    while ((CharInt = getchar()) && (char) CharInt != '\n' && CharInt != EOF) {
        PostArray[Length++] = (char) CharInt;
    }
    node *Tree = MakeTree(NULL, Length, InArray, 0, Length - 1, PostArray, 0, Length - 1);
    PrintPreOrder(Tree);
    printf("\n");
    return 0;
}