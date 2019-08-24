%{
	#include <stdio.h>
	#include "pascal_parser.h"
%}

%token	STD_FUNC STD_READ_PROC STD_READLN_PROC
%token	STD_PROC STD_WRITE_PROC STD_WRITELN_PROC
%token	FALSE TRUE CHSTR UINT UREAL IDENT

%token	T_boolean T_char T_integer T_real T_string
%token	K_array K_begin K_case K_const K_do K_downto K_else K_end K_file K_for
%token	K_function K_goto K_if K_label K_nil K_of K_packed K_procedure K_program
%token	K_record K_repeat K_set K_then K_to K_type K_until K_var K_while K_with

%token	ASG RNG CMM CLN SMC
%left	EQ LT GT NE LE GE K_in
%left	ADD SUB K_or
%left	MUL DIV K_and K_div K_mod
%right	PTR K_not
%left	LPR RPR LSB RSB DOT

%start program

%%

actual_parameter
: expression
| STD_PROC
;

actual_parameter_list
: actual_parameter_list CMM actual_parameter
| actual_parameter
;

adding_operator
: ADD
| SUB
| K_or
;

array_type
: K_array LSB ordinal_type_list RSB K_of type_denoter
;

array_type_identifier
: T_string
;

assignment_statement
: variable_access ASG expression
| STD_FUNC ASG expression
;

block
: label_block constant_block type_block variable_block caller_block main_block
;

boolean_value
: FALSE
| TRUE
;

caller_block
: caller_declarations
|
;

caller_declarations
: caller_declarations procedure_declaration
| caller_declarations function_declaration
| procedure_declaration SMC
| function_declaration SMC
;

caller_designator
: identifier LPR actual_parameter_list RPR
| identifier LPR RPR
;

case_list_element
: constant_list CLN statement
;

case_list_elements
: case_list_elements SMC case_list_element
| case_list_element
;

case_statement
: K_case expression K_of case_list_elements SMC K_end
| K_case expression K_of case_list_elements K_end
;

character_string
: CHSTR
;

compound_statement
: K_begin statement_sequence K_end
;

conditional_statement
: if_statement
| case_statement
;

conformant_array_schema
: packed_conformant_array_schema
| unpacked_conformant_array_schema
;

conformant_array_specification
: value_conformant_array_specification
| variable_conformant_array_specification
;

constant
: signed_number
| unsigned_number
| boolean_value
| sign identifier
| identifier
| character_string
;

constant_block
: K_const constant_definitions
|
;

constant_definition
: identifier EQ constant
;

constant_definitions
: constant_definitions constant_definition SMC
| constant_definition SMC
;

constant_list
: constant_list CMM constant
| constant
;

directive
: IDENT
;

else_part
: K_else statement
;

empty_statement
:
;

enumerated_type
: LPR identifier_list RPR
;

expression
: simple_expression relational_operator simple_expression
| simple_expression
;

expression_list
: expression_list CMM expression
| expression
;

factor
: K_not factor
| unsigned_constant
| variable_access
| function_designator
| caller_designator
| set_constructor
| LPR expression RPR
;

field_designator
: variable_access DOT identifier
;

field_list
: record_sections SMC variant_part SMC
| record_sections SMC
| variant_part SMC
| record_sections SMC variant_part
| record_sections
| variant_part
|
;

file_type
: K_file K_of type_denoter
;

for_statement
: K_for identifier ASG expression K_to expression K_do statement
| K_for identifier ASG expression K_downto expression K_do statement
;

formal_parameter_list
: formal_parameter_list SMC formal_parameter_section
| formal_parameter_section
;

formal_parameter_section
: conformant_array_specification
| value_parameter_specification
| variable_parameter_specification
| procedure_heading
| function_heading
;

function_declaration
: function_heading SMC directive
| function_heading SMC block
;

function_designator
: function_identifier LPR actual_parameter_list RPR
| function_identifier LPR RPR
| function_identifier
;

function_heading
: K_function identifier LPR formal_parameter_list RPR CLN type_identifier
| K_function identifier LPR RPR CLN type_identifier
| K_function identifier CLN type_identifier
;

function_identifier
: STD_FUNC
;

goto_statement
: K_goto label
;

identified_variable
: variable_access PTR
;

identifier
: IDENT
;

identifier_list
: identifier_list CMM identifier
| identifier
;

if_statement
: K_if expression K_then statement else_part
| K_if expression K_then statement
;

index_type_specification
: identifier RNG identifier CLN ordinal_type_identifier
;

index_type_specifications
: index_type_specifications SMC index_type_specification
| index_type_specification
;

indexed_variable
: variable_access LSB expression_list RSB
;

label
: identifier
| unsigned_integer
;

label_block
: K_label label_list SMC
| 
;

label_list
: label_list CMM label
| label
;

main_block
: compound_statement
;

member_designator
: expression RNG expression
| expression
;

member_designator_list
: member_designator_list CMM member_designator
| member_designator
;

multiplying_operator
: MUL
| DIV
| K_div
| K_mod
| K_and
;

new_ordinal_type
: enumerated_type
| subrange_type
;

new_pointer_type
: PTR type_identifier
;

new_structured_type
: K_packed unpacked_structured_type
| unpacked_structured_type
;

new_type
: new_ordinal_type
| new_structured_type
| new_pointer_type
;

ordinal_type
: new_ordinal_type 
| ordinal_type_identifier
;

ordinal_type_identifier
: T_boolean
| T_char
| T_integer
;

ordinal_type_list
: ordinal_type_list CMM ordinal_type
| ordinal_type
;

packed_conformant_array_schema
: K_packed K_array LSB index_type_specification RSB K_of type_identifier
;

procedure_declaration
: procedure_heading SMC directive
| procedure_heading SMC block
;

procedure_heading
: K_procedure identifier LPR formal_parameter_list RPR
| K_procedure identifier LPR RPR
| K_procedure identifier
;

procedure_identifier
: STD_PROC
| IDENT
;

procedure_statement
: procedure_identifier LPR actual_parameter_list RPR
| procedure_identifier LPR RPR
| procedure_identifier
;

program
: program_heading SMC block DOT
|
;

program_heading
: K_program identifier LPR identifier_list RPR
| K_program identifier
;

read_procedure_statement
: STD_READ_PROC LPR variable_access_list RPR
;

readln_procedure_statement
: STD_READLN_PROC LPR variable_access_list RPR
| STD_READLN_PROC LPR RPR
| STD_READLN_PROC
;

real_type_identifier
: T_real
;

record_section
: identifier_list CLN type_denoter
;

record_sections
: record_sections SMC record_section
| record_section
;

record_type
: K_record field_list K_end
;

relational_operator
: EQ
| NE
| LT
| GT
| LE
| GE
| K_in
;

repeat_statement
: K_repeat statement_sequence K_until expression
;

repetitive_statement
: repeat_statement
| while_statement
| for_statement
;

set_constructor
: LSB member_designator_list RSB
| LSB RSB
;

set_type
: K_set K_of ordinal_type
;

sign
: ADD
| SUB
;

signed_integer
: sign unsigned_integer
;

signed_number
: signed_integer
| signed_real
;

signed_real
: sign unsigned_real
;

simple_expression
: sign terms
| terms
;

simple_statement
: empty_statement
| assignment_statement
| read_procedure_statement
| readln_procedure_statement
| write_procedure_statement
| writeln_procedure_statement
| procedure_statement
| goto_statement
;

simple_type_identifier
: ordinal_type_identifier
| real_type_identifier
;

statement
: label CLN simple_statement
| label CLN structured_statement
| simple_statement
| structured_statement
;

statement_sequence
: statement_sequence SMC statement
| statement
;

structured_statement
: compound_statement
| conditional_statement
| repetitive_statement
| with_statement
;

subrange_type
: constant RNG constant
;

term
: term multiplying_operator factor
| factor
;

terms
: terms adding_operator term
| term
;

type_block
: K_type type_definitions
|
;

type_definition
: identifier EQ type_denoter
;

type_definitions
: type_definitions type_definition SMC
| type_definition SMC
;

type_denoter
: type_identifier
| new_type
;

type_identifier
: simple_type_identifier
| array_type_identifier
| identifier
;

unpacked_conformant_array_schema
: K_array LSB index_type_specifications RSB K_of type_identifier
| K_array LSB index_type_specifications RSB K_of conformant_array_schema
;

unpacked_structured_type
: array_type
| record_type
| set_type
| file_type
;

unsigned_constant
: unsigned_number
| boolean_value
| character_string
| K_nil
;

unsigned_integer
: UINT
;

unsigned_number
: unsigned_integer
| unsigned_real
;

unsigned_real
: UREAL
;

value_conformant_array_specification
: identifier_list CLN conformant_array_schema
;

value_parameter_specification
: identifier_list CLN type_identifier
;

variable_access
: identifier
| indexed_variable
| field_designator
| identified_variable
;

variable_access_list
: variable_access_list CMM variable_access
| variable_access
;

variable_block
: K_var variable_declarations
|
;

variable_conformant_array_specification
: K_var identifier_list CLN conformant_array_schema
;

variable_declaration
: identifier_list CLN type_denoter
;

variable_declarations
: variable_declarations variable_declaration SMC
| variable_declaration SMC
;

variable_parameter_specification
: K_var identifier_list CLN type_identifier
;

variant
: constant_list CLN LPR field_list RPR
;

variant_part
: K_case variant_selector K_of variants
;

variant_selector
: identifier CLN ordinal_type_identifier
| ordinal_type_identifier
;

variants
: variants SMC variant
| variant
;

while_statement
: K_while expression K_do statement
;

with_statement
: K_with variable_access_list K_do statement
;

write_parameter
: expression CLN expression CLN expression
| expression CLN expression
| expression
;

write_parameter_list
: variable_access CMM write_parameters
| write_parameters
;

write_parameters
: write_parameters CMM write_parameter
| write_parameter
;

write_procedure_statement
: STD_WRITE_PROC LPR write_parameter_list RPR
;

writeln_parameter_list
: variable_access CMM write_parameters
| write_parameters
;

writeln_procedure_statement
: STD_WRITELN_PROC LPR writeln_parameter_list RPR
| STD_WRITELN_PROC LPR RPR
| STD_WRITELN_PROC
;

%%

void yyerror(char const *s) {
	fprintf(stderr, "%s\n", s);
}
