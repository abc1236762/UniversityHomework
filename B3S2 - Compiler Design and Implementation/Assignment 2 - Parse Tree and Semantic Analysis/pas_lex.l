%{
#include <stdio.h>
#include <string.h>
#include "pascal.h"
#include "pas_tree.h"
#include "pas_yacc.h"
%}

ID  [A-Za-z][A-Za-z0-9]*
NUM [0-9][0-9]*
STR '([^']|'')*'

%%

div			{return DIV;}
or			{return OR;}
and			{return AND;}
not			{return NOT;}
if			{return IF;}
then		{return THEN;}
else		{return ELSE;}
of			{return OF;}
while		{return WHILE;}
do			{return DO;}
begin		{return BG;}
end			{return END;}
read		{return READ;}
write		{return WRITE;}
var			{return VAR;}
array		{return ARRAY;}
procedure	{return PROC;}
program		{return PROG;}
integer		{return INT;}
Boolean		{return BOOL;}
true		{return TRUE;}
false		{return FALSE;}
"+"			{return ADD;}
"-"			{return MINUS;}
"*"			{return TIMES;}
"="			{return EQ;}
"<>"		{return NE;}
"<"			{return LT;}
">"			{return GT;}
"<="		{return LE;}
">="		{return GE;}
"("			{return LP;}
")"			{return RP;}
"["			{return LSP;}
"]"			{return RSP;}
":="		{return ASSIGN;}
"."			{return DOT;}
","			{return COMMA;}
":"			{return COLON;}
";"			{return SEMI;}
".."		{return DOTDOT;}

{ID}		{
	yylval.str = strdup(yytext);
	return ID;
}

{NUM}		{
	sscanf(yytext, "%d", &pas_val);
	yylval.num = pas_val;
	return NUM;
}

{STR}		{
	yylval.str = strdup(yytext);
	return STR;
}

[ \t\n]		{ }

%%

int yywrap() {
	return 1;
}
