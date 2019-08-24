#include <stdio.h>
#include "pascal_yacc.h"
#include "pascal_parser.h"

int main(int argc, char **argv) {
	yyin = fopen(argv[1], "r");
	/*
	int token;
	while ((token = yylex()) != 0)
		printf("Got token %d: %s\n", token, yytext);
	
	printf("\n");
	*/
	yyparse();
	
	return 0;
}
