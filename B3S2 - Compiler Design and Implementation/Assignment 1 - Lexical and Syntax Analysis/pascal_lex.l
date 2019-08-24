%{
	#include "pascal_parser.h"
	#include "pascal_yacc.h"
	
	void comment();
%}

D				[[:digit:]]+
E				[Ee][+-]?{D}

IDENT			[[:alpha:]][[:alnum:]]*
UINT			{D}
UREAL			{D}(\.{D}{E}?|{E})
CHSTR			'([^']|'')*'

%%

"="				return EQ;
"<"				return LT;
">"				return GT;
"<>"			return NE;
"<="			return LE;
">="			return GE;
"+"				return ADD;
"-"				return SUB;
"*"				return MUL;
"/"				return DIV;
":="			return ASG;
".."			return RNG;
"^"|"@"			return PTR;
"("				return LPR;
")"				return RPR;
"["|"(."		return LSB;
"]"|".)"		return RSB;
"."				return DOT;
","				return CMM;
":"				return CLN;
";"				return SMC;

"and"			return K_and;
"array"			return K_array;
"begin"			return K_begin;
"case"			return K_case;
"const"			return K_const;
"div"			return K_div;
"do"			return K_do;
"downto"		return K_downto;
"else"			return K_else;
"end"			return K_end;
"file"			return K_file;
"for"			return K_for;
"function"		return K_function;
"goto"			return K_goto;
"if"			return K_if;
"in"			return K_in;
"label"			return K_label;
"mod"			return K_mod;
"nil"			return K_nil;
"not"			return K_not;
"of"			return K_of;
"or"			return K_or;
"packed"		return K_packed;
"procedure"		return K_procedure;
"program"		return K_program;
"record"		return K_record;
"repeat"		return K_repeat;
"set"			return K_set;
"then"			return K_then;
"to"			return K_to;
"type"			return K_type;
"until"			return K_until;
"var"			return K_var;
"while"			return K_while;
"with"			return K_with;

"Boolean"		return T_boolean;
"char"			return T_char;
"integer"		return T_integer;
"real"			return T_real;
"string"		return T_string;

"abs"			|
"arctan"		|
"chr"			|
"cos"			|
"eof"			|
"eoln"			|
"exp"			|
"ln"			|
"odd"			|
"ord"			|
"pred"			|
"round"			|
"sin"			|
"sqr"			|
"sqrt"			|
"succ"			|
"trunc"			return STD_FUNC;

"dispose"		|
"get"			|
"new"			|
"pack"			|
"page"			|
"put"			|
"reset"			|
"rewrite"		|
"unpack"		return STD_PROC;
"read"			return STD_READ_PROC;
"readln"		return STD_READLN_PROC;
"write"			return STD_WRITE_PROC;
"writeln"		return STD_WRITELN_PROC;

"false"			return FALSE;
"true"			return TRUE;
{CHSTR}			return CHSTR;
{UINT}			return UINT;
{UREAL}			return UREAL;

{IDENT}			return IDENT;
[ \f\n\r\t\v​]	;			// Whitespaces
"{"|"(*"		comment();	// Comments

%%

void comment() {
	char ch;
	while (1) {
		while ((ch = input()) != EOF && ch != '}' && ch != '*');
		if (ch == '}') {
			return;
		} else if (ch == '*') {
			while ((ch = input()) != EOF && ch == '*');
			if (ch == ')') return;
		}
		if (ch == EOF) {
			yyerror("EOF in comment");
			return;
		}
	}
}

int yywrap(void) {
	return 1;
}
