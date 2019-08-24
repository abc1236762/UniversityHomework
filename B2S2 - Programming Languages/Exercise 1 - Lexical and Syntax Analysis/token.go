// Parser Implementation Homework
// Written by 410521209 林鈺錦
// GNU General Public License v3.0
//
// token.go defines data structures about a token and token names.

package main

// TknName is an enum type to list all tokens.
type TknName int

// Values of enum TknName.
const (
	_     TknName = iota
	OpAdd  // '+' operator
	OpSub  // '-' operator
	OpMlt  // '*' operator
	OpDiv  // '/' operator
	OpCrt  // '^' operator
	SpLpr  // '(' separator
	SpRpr  // ')' separator
	SpSem  // ';' separator
	ItInt  // integer literal
	ItFlt  // float literal
	Ident  // identifier
	Eof    // end of file
	Exprs  // <exprs>
	Expr   // <expr>
	Term   // <term>
	Fctr   // <fctr>
	Exp    // <exp>
)

// TknName.Name returns the string of token name.
func (tn TknName) Name() string {
	return map[TknName]string{
		OpAdd: "OP_ADD",
		OpSub: "OP_SUB",
		OpMlt: "OP_MLT",
		OpDiv: "OP_DIV",
		OpCrt: "OP_CRT",
		SpLpr: "SP_LPR",
		SpRpr: "SP_RPR",
		SpSem: "SP_SEM",
		ItInt: "IT_INT",
		ItFlt: "IT_FLT",
		Ident: "IDENT",
		Eof:   "EOF",
		Exprs: "<exprs>",
		Expr:  "<expr>",
		Term:  "<term>",
		Fctr:  "<fctr>",
		Exp:   "<exp>",
	}[tn]
}

// Token is a struct to save token name and token value
// with reference to code string or the parsing error.
type Token struct {
	Name TknName
	Val  []rune
}

// NewToken makes a token and return the pointer.
func NewToken(name TknName, val []rune) (tkn *Token) {
	return &Token{name, val}
}

// Token.IsName judge the token name is in these name or not.
func (t *Token) IsName(name ... TknName) bool {
	for _, n := range name {
		if n == t.Name {
			return true
		}
	}
	return false
}
