#include "pas_tree.h"

typedef enum { T_INT, T_STR, T_BOOL } type_t;

typedef struct {
	type_t type;
	char name[16];
} ident_t;

typedef struct {
	int ident_no;
	int idx_begin;
	int length;
} array_t;

type_t ident_type_now;
int array_idx_begin_now;
int array_length_now;
int idents_cnt = 0;
ident_t idents[16];
int arrays_cnt = 0;
array_t arrays[16];
int tabs_cnt = 0;

bool is_defining_arrays = false;
bool is_defining_proces = false;
bool is_doing_scanf = false;
bool is_doing_printf = false;
bool is_doing_expr = false;
bool is_doing_array = false;
bool is_semi_needed = true;

char scpr_fmts_buf[1024];
char scpr_args_buf[1024];
char array_buf[1024];
char expr_buf[1024];

int get_ident_no(char *ident_name) {
	for (int i = 0; i < idents_cnt; i++) {
		if (strcmp(ident_name, idents[i].name) == 0)
			return i;
	}
	return -1;
}

type_t judge_type(char *ident_name) {
	if (ident_name) {
		int ident_no = get_ident_no(ident_name);
		return idents[ident_no].type;
	}
	if (expr_buf[strlen(expr_buf) - 1] == ']') {
		int rsb_conut = 0;
		for (int i = 0; i < strlen(expr_buf); i++)
			if (expr_buf[i] == ']')
				rsb_conut += 1;
		if (rsb_conut > 1)
			return T_INT;
		char array_ident[16] = "";
		for (int i = 0; i < 16; i++) {
			if (expr_buf[i] == ' ')
				return T_INT;
			else if (expr_buf[i] == '[')
				break;
			array_ident[i] = expr_buf[i];
		}
		return judge_type(array_ident);
	} else if (strstr(expr_buf, "true") && strstr(expr_buf, "false")) {
		return T_BOOL;
	} else if (expr_buf[0] == '"' && expr_buf[strlen(expr_buf) - 1] == '"') {
		return T_STR;
	} else {
		return T_INT;
	}
}

void clear_scpr_bufs(void) {
	memset(scpr_fmts_buf, '\0', sizeof(scpr_fmts_buf));
	memset(scpr_args_buf, '\0', sizeof(scpr_args_buf));
}

void clear_expr_buf(void) {
	memset(expr_buf, '\0', sizeof(expr_buf));
}

void push_tabs() {
	for (int i = 0; i < tabs_cnt; i++)
		fprintf(yyout, "\t");
}

void push_expr() {
	fputs(expr_buf, yyout);
	clear_expr_buf();
}

void push_fmt(char *ident_name, bool is_scan) {
	type_t type = judge_type(ident_name);
	if (strlen(scpr_fmts_buf) != 0)
		strcat(scpr_fmts_buf, " ");
	if (type == T_INT)
		strcat(scpr_fmts_buf, "%d");
	else if (type == T_STR)
		strcat(scpr_fmts_buf, "%s");
	else if (type == T_BOOL)
		if (is_scan)
			strcat(scpr_fmts_buf, "%d");
		else
			strcat(scpr_fmts_buf, "%s");
}

void push_arg(char *ident_name, bool is_scan) {
	type_t ident_type = judge_type(ident_name);
	if (strlen(scpr_args_buf) != 0)
		strcat(scpr_args_buf, ", ");
	if (is_scan && (ident_type == T_INT || ident_type == T_BOOL))
		strcat(scpr_args_buf, "&");
	if (ident_name) {
		strcat(scpr_args_buf, ident_name);
		if (ident_type == T_BOOL && !is_scan)
			strcat(scpr_args_buf, " ? \"true\" : \"false\"");
	} else {
		strcat(scpr_args_buf, expr_buf);
		clear_expr_buf();
	}
}

void push_array_arg_front(char *ident_name) {
	strcat(expr_buf, ident_name);
	strcat(expr_buf, "[");
}

void push_array_arg_rear(char *ident_name) {
	int ident_no = get_ident_no(ident_name);
	for (int i = 0; i < arrays_cnt; i++) {
		if (arrays[i].ident_no == ident_no) {
			if (arrays[i].idx_begin != 0) {
				if (arrays[i].idx_begin < 0)
					strcat(expr_buf, " + ");
				else
					strcat(expr_buf, " - ");
				char idx_begin_str[16];
				sprintf(idx_begin_str, "%d", abs(arrays[i].idx_begin));
				strcat(expr_buf, idx_begin_str);
			}
			strcat(expr_buf, "]");
			return;
		}
	}
}

pEXP *create_exp() {
	pEXP *tmp = (pEXP *)malloc(sizeof(pEXP));
	if (tmp) {
		tmp->exp_id = eMIN;
		tmp->str[0] = '\0';
		tmp->num = 0;
		tmp->exp1 = NULL;
		tmp->exp2 = NULL;
		tmp->next = NULL;
	}
	return tmp;
}

pSTM *create_stm() {
	pSTM *tmp = (pSTM *)malloc(sizeof(pSTM));
	if (tmp) {
		tmp->stm_id = sMIN;
		tmp->exp1 = NULL;
		tmp->exp2 = NULL;
		tmp->stm1 = NULL;
		tmp->stm2 = NULL;
		tmp->next = NULL;
	}
	return tmp;
}

void free_exp(pEXP *p) {
	if (p) {
		if (p->exp1)
			free_exp(p->exp1);
		if (p->exp2)
			free_exp(p->exp2);
		if (p->next)
			free_exp(p->next);
		free(p);
	}
}

void free_stm(pSTM *p) {
	if (p) {
		if (p->exp1)
			free_exp(p->exp1);
		if (p->exp2)
			free_exp(p->exp2);
		if (p->stm1)
			free_stm(p->stm1);
		if (p->stm2)
			free_stm(p->stm2);
		if (p->next)
			free_stm(p->next);
		free(p);
	}
}

void print_exp(pEXP *p) {
	pEXP *te;
	char str_temp[16];
	if (p) {
		switch (p->exp_id) {
		case eMOREID:
			fprintf(yyout, ", ");
			print_exp(p->exp1);
			break;
		case eARRTYPE:
			is_defining_arrays = true;
			print_exp(p->exp1);
			print_exp(p->exp2);
			break;
		case eINRANGE:
			array_idx_begin_now = p->num;
			array_length_now = p->exp1->num - p->num + 1;
			break;
		case eINT:
			fprintf(yyout, "int ");
			ident_type_now = T_INT;
			break;
		case eBOOL:
			fprintf(yyout, "bool ");
			ident_type_now = T_BOOL;
			break;
		case eMOREINVAR:
			print_exp(p->exp1);
			print_exp(p->next);
			break;
		case eMOREOUTVAL:
			print_exp(p->exp1);
			print_exp(p->next);
			break;
		case eEXPRESS:
			is_doing_expr = true;
			print_exp(p->exp1);
			if (p->exp2) {
				print_exp(p->exp2);
				print_exp(p->next);
			}
			is_doing_expr = false;
			if (!is_doing_array) {
				if (is_doing_printf) {
					push_fmt(NULL, false);
					push_arg(NULL, false);
				} else if (!is_doing_scanf) {
					push_expr();
				}
			}
			break;
		case eSIMEXPRE:
			print_exp(p->exp1);
			print_exp(p->exp2);
			print_exp(p->next);
			break;
		case eADDTERM:
			print_exp(p->exp1);
			print_exp(p->exp2);
			print_exp(p->next);
			break;
		case eTERM:
			print_exp(p->exp1);
			print_exp(p->exp2);
			break;
		case eMULTIFAC:
			print_exp(p->exp1);
			print_exp(p->exp2);
			print_exp(p->next);
			break;
		case eLPRP:
			strcat(expr_buf, "(");
			print_exp(p->exp1);
			strcat(expr_buf, ")");
			break;
		case eNOT:
			strcat(expr_buf, "!");
			print_exp(p->exp1);
			break;
		case eADD:
			strcat(expr_buf, " + ");
			break;
		case eMINUS:
			strcat(expr_buf, " - ");
			break;
		case eNOSIGN:
			break;
		case eOR:
			strcat(expr_buf, " || ");
			break;
		case eTIMES:
			strcat(expr_buf, " * ");
			break;
		case eDIV:
			strcat(expr_buf, " / ");
			break;
		case eAND:
			strcat(expr_buf, " && ");
			break;
		case eINDEXVAR:
			strcpy(str_temp, p->exp1->str);
			push_array_arg_front(str_temp);
			is_doing_array = true;
			print_exp(p->exp2);
			is_doing_array = false;
			push_array_arg_rear(str_temp);
			if (is_doing_scanf) {
				push_fmt(str_temp, true);
				push_arg(NULL, true);
			} else if (!is_doing_printf) {
				push_expr();
			}
			break;
		case eNUM:
			sprintf(str_temp, "%d", p->num);
			strcat(expr_buf, str_temp);
			break;
		case eSTR:
			p->str[0] = '"';
			p->str[strlen(p->str) - 1] = '"';
			strcat(expr_buf, p->str);
			break;
		case eTRUE:
			strcat(expr_buf, "true");
			break;
		case eFALSE:
			strcat(expr_buf, "false");
			break;
		case eEQ:
			strcat(expr_buf, " == ");
			break;
		case eNE:
			strcat(expr_buf, " != ");
			break;
		case eLT:
			strcat(expr_buf, " < ");
			break;
		case eGT:
			strcat(expr_buf, " > ");
			break;
		case eLE:
			strcat(expr_buf, " <= ");
			break;
		case eGE:
			strcat(expr_buf, " >= ");
			break;
		case eID:
			if (is_doing_expr || is_doing_array) {
				strcat(expr_buf, p->str);
			} else if (is_doing_scanf) {
				push_fmt(p->str, true);
				push_arg(p->str, true);
			} else {
				fprintf(yyout, "%s", p->str);
			}
			break;
		case eVARDEC:
			fprintf(yyout, "%s", p->str);
			idents[idents_cnt].type = ident_type_now;
			strcpy(idents[idents_cnt].name, p->str);
			if (is_defining_arrays) {
				arrays[arrays_cnt].ident_no = idents_cnt;
				arrays[arrays_cnt].idx_begin = array_idx_begin_now;
				arrays[arrays_cnt].length = array_length_now;
				fprintf(yyout, "[%d]", arrays[arrays_cnt].length);
				arrays_cnt += 1;
			}
			idents_cnt += 1;
			print_exp(p->next);
			break;
		default:
			fprintf(stderr, "Fatal: has an error in expressions.\n");
			break;
		}
	}
}

void print_stm(pSTM *p) {
	pEXP *te;
	pSTM *ts;
	if (p) {
		switch (p->stm_id) {
		case sPROG:
			clear_scpr_bufs();
			clear_expr_buf();
			fprintf(yyout, "#ifndef _%s_\n", p->exp1->str);
			fprintf(yyout, "#define _%s_\n", p->exp1->str);
			fprintf(yyout, "#endif\n\n");
			fprintf(yyout, "#include <stdio.h>\n");
			fprintf(yyout, "#include <stdlib.h>\n");
			fprintf(yyout, "#include <stdbool.h>\n\n");
			print_stm(p->stm1);
			break;
		case sBLOCK:
			print_stm(p->stm1);
			print_stm(p->stm2);
			if (!is_defining_proces) {
				fprintf(yyout, "int main(void) {\n");
				tabs_cnt += 1;
			}
			print_stm(p->next);
			if (!is_defining_proces)
				fprintf(yyout, "\treturn 0;\n}\n");
			break;
		case sVARDECS:
			print_stm(p->stm1);
			print_stm(p->next);
			fprintf(yyout, "\n");
			break;
		case sMOREVD:
			print_stm(p->stm1);
			print_stm(p->next);
			break;
		case sVARDEC:
			print_exp(p->exp2);
			print_exp(p->exp1);
			fprintf(yyout, ";\n");
			is_defining_arrays = false;
			break;
		case sPRODECS:
			is_defining_proces = true;
			print_stm(p->stm1);
			print_stm(p->next);
			is_defining_proces = false;
			break;
		case sPROC:
			push_tabs();
			fprintf(yyout, "void %s(void) {\n", p->exp1->str);
			tabs_cnt += 1;
			print_stm(p->stm1);
			tabs_cnt -= 1;
			push_tabs();
			fprintf(yyout, "}\n\n");
			break;
		case sCOMSTMT:
			print_stm(p->stm1);
			if (is_semi_needed)
				fprintf(yyout, ";\n");
			is_semi_needed = true;
			print_stm(p->stm2);
			break;
		case sMORESTM:
			print_stm(p->stm1);
			if (is_semi_needed)
				fprintf(yyout, ";\n");
			is_semi_needed = true;
			print_stm(p->next);
			break;
		case sASSTATE:
			push_tabs();
			print_exp(p->exp1);
			fprintf(yyout, " = ");
			print_exp(p->exp2);
			break;
		case sPROSTATE:
			push_tabs();
			fprintf(yyout, "%s()", p->exp1->str);
			break;
		case sRESTATE:
			push_tabs();
			is_doing_scanf = true;
			clear_scpr_bufs();
			print_exp(p->exp1);
			print_exp(p->exp2);
			fputs("scanf(\"", yyout);
			fputs(scpr_fmts_buf, yyout);
			fputs("\", ", yyout);
			fputs(scpr_args_buf, yyout);
			fputs(")", yyout);
			is_doing_scanf = false;
			break;
		case sWRISTATE:
			push_tabs();
			is_doing_printf = true;
			clear_scpr_bufs();
			print_exp(p->exp1);
			print_exp(p->exp2);
			fputs("printf(\"", yyout);
			fputs(scpr_fmts_buf, yyout);
			fputs("\\n\", ", yyout);
			fputs(scpr_args_buf, yyout);
			fputs(")", yyout);
			is_doing_printf = false;
			break;
		case sIFSTATE:
			push_tabs();
			fprintf(yyout, "if (");
			print_exp(p->exp1);
			fprintf(yyout, ") {\n");
			tabs_cnt += 1;
			print_stm(p->stm1);
			fprintf(yyout, ";\n");
			tabs_cnt -= 1;
			push_tabs();
			fprintf(yyout, "}");
			if (p->stm2) {
				fprintf(yyout, " else {\n");
				tabs_cnt += 1;
				print_stm(p->stm2);
				tabs_cnt -= 1;
				push_tabs();
				fprintf(yyout, "}");
			}
			fprintf(yyout, "\n");
			is_semi_needed = false;
			break;
		case sWHILEST:
			push_tabs();
			fprintf(yyout, "while (");
			print_exp(p->exp1);
			fprintf(yyout, ") {\n");
			tabs_cnt += 1;
			print_stm(p->stm1);
			tabs_cnt -= 1;
			push_tabs();
			fprintf(yyout, "}\n");
			is_semi_needed = false;
			break;
		default:
			fprintf(stderr, "******* An error in statements!\n");
			break;
		}
	}
}
