// Parser Implementation Homework
// Written by 410521209 林鈺錦
// GNU General Public License v3.0
//
// parser.go define Parser class and the functions for doing syntactic analysis.

package main

import (
	"fmt"
	"strconv"
	"strings"
	
	"github.com/xlab/treeprint"
)

// PrsNode is a struct to save the token and child nodes.
type PrsNode struct {
	Childs []*PrsNode
	Tkn    *Token
}

// PrsNode.addChild adds and returns a child node with token name and value.
func (pn *PrsNode) addChild(tkn *Token) (node *PrsNode) {
	node = &PrsNode{make([]*PrsNode, 0), tkn}
	pn.Childs = append(pn.Childs, node)
	return
}

// PrsNode.uniteChildsRunes unites token values of all children to own’s.
func (pn *PrsNode) uniteChildsRunes(runes []rune) {
	var firstRunes = pn.Childs[0].Tkn.Val
	var lastRunes = pn.Childs[len(pn.Childs)-1].Tkn.Val
	var startIdx = RunesFromIdx(runes, firstRunes)
	var endIdx = RunesFromIdx(runes, lastRunes) + len(lastRunes)
	pn.Tkn.Val = runes[startIdx:endIdx]
}

// PrsErrKind is an enum type to list all kinds of parse error.
type PrsErrKind int

// Values of enum PrsErrKind.
const (
	_         PrsErrKind = iota
	ExpcOp     // expecting operator
	ExpcSpLpr  // expecting '(' separator
	ExpcSpRpr  // expecting ')' separator
	ExpcSpSem  // expecting ';' separator
	ExpcExpr   // expecting expression
)

// PrsErrKind.String returns the string of type of parse error kind.
func (pek PrsErrKind) String() string {
	return map[PrsErrKind]string{
		ExpcOp:    `expecting operator`,
		ExpcSpLpr: `expecting "("`,
		ExpcSpRpr: `expecting ")"`,
		ExpcSpSem: `expecting ";"`,
		ExpcExpr:  `expecting expression`,
	}[pek]
}

// PrsErr is a class implement builtin.error interface to store a parsing error.
type PrsErr struct {
	Lxr  *Lexer
	Tkn  *Token
	Kind PrsErrKind
}

// PrsErr.Error returns a string to show the error details.
func (pe *PrsErr) Error() (errStr string) {
	var startCol, startLn = len(pe.Lxr.Runes), 0
	var endCol, endLn = startCol, startLn
	if pe.Tkn.Name != Eof {
		startCol = RunesFromIdx(pe.Lxr.Runes, pe.Tkn.Val)
		endCol = startCol + len(pe.Tkn.Val) - 1
	}
	for i, line := range strings.Split(string(pe.Lxr.Runes), "\n") {
		if startCol >= len(line+"\n") {
			startCol -= len(line + "\n")
			startLn = i + 1
		}
		if endCol >= len(line+"\n") {
			endCol -= len(line + "\n")
			endLn = i + 1
		}
	}
	var lines = strings.Split(string(pe.Lxr.Runes), "\n")[startLn : endLn+1]
	var tknVal = `"` + UnescapeStr(string(pe.Tkn.Val)) + `"`
	if pe.Tkn.Name == Eof {
		tknVal = Eof.Name()
	}
	errStr = fmt.Sprintf("syntax error: unexpected %s, %s",
		tknVal, pe.Kind.String())
	errStr += fmt.Sprintf(" from line %d, column %d to line %d, column %d.\n",
		startLn+1, startCol+1, endLn+1, endCol+1)
	for i, ln := range lines {
		errStr += fmt.Sprintf(" %3d: %s\n", startLn+i+1, ln)
		if i == 0 {
			errStr += fmt.Sprintf("%6s%"+strconv.Itoa(startCol+1)+"s", " ", "^")
			if len(lines) == 1 {
				for i := 0; i < len(pe.Tkn.Val)-1; i++ {
					errStr += "~"
				}
			} else {
				for i := 0; i < len([]rune(ln))-startCol-1; i++ {
					errStr += "~"
				}
			}
		} else if i == len(lines)-1 {
			errStr += fmt.Sprintf("%6s", " ")
			for i := 0; i < endCol+1; i++ {
				errStr += "~"
			}
		} else {
			errStr += fmt.Sprintf("%6s", " ")
			for i := 0; i < len([]rune(ln)); i++ {
				errStr += "~"
			}
		}
		errStr += "\n"
	}
	return
}

// Parser is a class to parse code, it has the
// root node of the parse tree and the code string.
type Parser struct {
	Code     string
	Lxr      *Lexer
	TreeRoot *PrsNode
	TknIdx   int
	Errs     []*PrsErr
}

// NewParser makes a parser with the code
// string and a lexer and return the pointer.
func NewParser(code string, canNumNeg bool) (psr *Parser) {
	return &Parser{
		Code:     code,
		Lxr:      &Lexer{[]rune(code), make([]*Token, 0), canNumNeg},
		TreeRoot: &PrsNode{nil, &Token{Name: Exprs}},
		Errs:     make([]*PrsErr, 0),
	}
}

// Parser.Parse parses the code.
func (p *Parser) Parse() {
	p.prsExprs(p.TreeRoot)
	return
}

// Parser.NextTkn gets the next token.
func (p *Parser) NextTkn() *Token {
	if p.TknIdx < len(p.Lxr.Tkns) {
		p.TknIdx++
	}
	return p.Lxr.Tkns[p.TknIdx-1]
}

// Parser.SprintTree returns the formatted string to show the parse tree.
func (p *Parser) SprintTree() string {
	treeprint.EdgeTypeStart = treeprint.EdgeType(Exprs.Name())
	var printer = treeprint.New()
	var fmtStr = func(tkn *Token) (s string) {
		s = strings.TrimRight(fmt.Sprintf("%-7s", tkn.Name.Name()), " ")
		if len(tkn.Val) > 0 {
			s += ` ── "` + UnescapeStr(string(tkn.Val)) + `"`
		}
		return
	}
	var build func(*PrsNode, treeprint.Tree)
	build = func(node *PrsNode, printer treeprint.Tree) {
		for _, node := range node.Childs {
			var printer = printer.AddBranch(fmtStr(node.Tkn))
			build(node, printer)
		}
	}
	build(p.TreeRoot, printer)
	return "—Parse Tree:\n" + printer.String() + "\n"
}

func (p *Parser) addErr(tkn *Token, kind PrsErrKind) {
	p.Errs = append(p.Errs, &PrsErr{p.Lxr, tkn, kind})
}

// Parser.prsExprs parses <exprs> using following rule.
// <exprs> → <expr> ';' { <expr> ';' }
// ↔ <exprs> → <expr> ';' <exprs> | <expr> ';'
func (p *Parser) prsExprs(node *PrsNode) {
	p.prsExpr(node.addChild(NewToken(Expr, nil)))
	if NextTkn := p.NextTkn(); NextTkn.IsName(SpSem) {
		node.addChild(NextTkn)
		if NextTkn := p.NextTkn(); NextTkn.Name != Eof {
			p.TknIdx--
			p.prsExprs(node.addChild(NewToken(Exprs, nil)))
		} else {
			// The parsing is finished.
			return
		}
	} else {
		if NextTkn.IsName(SpRpr) {
			// Add a syntax error with expecting expecting `(`.
			p.addErr(NextTkn, ExpcSpLpr)
		} else {
			// Add a syntax error with expecting expecting `;`.
			p.addErr(NextTkn, ExpcSpSem)
		}
	}
	return
}

// Parser.prsExpr parses <expr> using following rule.
// <expr> → <term> { ( '+' | '-' ) <term> }
// ↔ <expr> → <term> ( '+' | '-' ) <expr> | <term>
func (p *Parser) prsExpr(node *PrsNode) {
	p.prsTerm(node.addChild(NewToken(Term, nil)))
	if NextTkn := p.NextTkn(); NextTkn.IsName(OpAdd, OpSub) {
		node.addChild(NextTkn)
		if NextTkn := p.NextTkn(); NextTkn.Name != Eof {
			p.TknIdx--
			p.prsExpr(node.addChild(NewToken(Expr, nil)))
		} else {
			// Add a syntax error with expecting expression.
			p.addErr(NextTkn, ExpcExpr)
		}
	} else if NextTkn.IsName(SpSem, SpRpr, OpMlt, OpDiv, OpCrt) {
		p.TknIdx--
		return
	} else {
		if NextTkn.Name != Eof {
			// Add a syntax error with expecting operator.
			p.addErr(NextTkn, ExpcOp)
		} else {
			p.TknIdx--
		}
	}
	return
}

// Parser.prsTerm parses <term> using following rule.
// <term> → <fctr> { ( '*' | '/' ) <fctr> }
// ↔ <term> → <fctr> ( '*' | '/' ) <term> | <fctr>
func (p *Parser) prsTerm(node *PrsNode) {
	p.prsFctr(node.addChild(NewToken(Fctr, nil)))
	if NextTkn := p.NextTkn(); NextTkn.IsName(OpMlt, OpDiv) {
		node.addChild(NextTkn)
		if NextTkn := p.NextTkn(); NextTkn.Name != Eof {
			p.TknIdx--
			p.prsTerm(node.addChild(NewToken(Term, nil)))
		} else {
			// Add a syntax error with expecting expression.
			p.addErr(NextTkn, ExpcExpr)
		}
	} else {
		p.TknIdx--
	}
	return
}

// Parser.prsFctr parses <fctr> using following rule.
// <fctr> → <exp> { '^' <exp> }
// ↔ <fctr> → <exp> '^' <fctr> | <exp>
func (p *Parser) prsFctr(node *PrsNode) {
	p.prsExp(node.addChild(NewToken(Exp, nil)))
	if NextTkn := p.NextTkn(); NextTkn.IsName(OpCrt) {
		node.addChild(NextTkn)
		if NextTkn := p.NextTkn(); NextTkn.Name != Eof {
			p.TknIdx--
			p.prsFctr(node.addChild(NewToken(Fctr, nil)))
		} else {
			// Add a syntax error with expecting expression.
			p.addErr(NextTkn, ExpcExpr)
		}
	} else {
		p.TknIdx--
	}
	return
}

// Parser.prsExp parses <exp> using following rule.
// <exp> → IDENT | IT_INT | IT_FLT | '(' <expr> ')'
func (p *Parser) prsExp(node *PrsNode) {
	if NextTkn := p.NextTkn(); NextTkn.IsName(Ident, ItInt, ItFlt) {
		node.addChild(NextTkn)
		return
	} else if NextTkn.IsName(SpLpr) {
		node.addChild(NextTkn)
		p.prsExpr(node.addChild(NewToken(Expr, nil)))
		if NextTkn := p.NextTkn(); NextTkn.IsName(SpRpr) {
			return
		} else {
			// Add a syntax error with expecting `)`.
			p.addErr(NextTkn, ExpcSpRpr)
		}
	} else {
		// Add a syntax error with expecting expression.
		p.addErr(NextTkn, ExpcExpr)
		p.TknIdx--
	}
	return
}
