// Parser Implementation Homework
// Written by 410521209 林鈺錦
// GNU General Public License v3.0
//
// lexer.go defines Lexer class and the functions for laxing and getting tokens.

package main

import (
	"fmt"
	"strings"
	"unicode"
)

// Lexer is a class to lexing the code, it has the rune array
// of the code string, the list of got tokens and a boolean
// to make the lexer allows number be negative or not.
type Lexer struct {
	Runes     []rune
	Tkns      []*Token
	CanNumNeg bool
}

// Lexer.Lex lexes the code.
func (l *Lexer) Lex() {
	var lastTkn, tkn *Token
	for {
		if tkn = l.lexEOF(); tkn == nil {
			if lastTkn != nil && lastTkn.IsName(Ident, SpRpr, ItInt, ItFlt) {
				if tkn = l.lexOpSp(); tkn == nil {
					tkn = l.lexIt()
				}
			} else {
				if tkn = l.lexIt(); tkn == nil {
					tkn = l.lexOpSp()
				}
			}
			if tkn == nil {
				tkn = l.lexIdent()
			}
		}
		l.Tkns = append(l.Tkns, tkn)
		lastTkn = tkn
		if tkn.Name == Eof {
			break
		}
	}
}

// SprintTkns returns the formatted string to show tokens.
func (l *Lexer) SprintTkns() (str string) {
	str = fmt.Sprintln("—Tokens:")
	for i, tkn := range l.Tkns {
		str += fmt.Sprintf("%3d. %-6s",
			i+1, tkn.Name.Name())
		if tkn.Val != nil {
			str += ` : "` + UnescapeStr(string(tkn.Val)) + `"`
		}
		str = strings.TrimRight(str, " ") + "\n"
	}
	return
}

// Lexer.unlexRunes gets rune array of the code that is not be lexed yet.
func (l *Lexer) unlexRunes() (runes []rune) {
	var lastTkn *Token
	
	// If tokens have something, runes starts
	// after the position of the last token.
	if len(l.Tkns) == 0 {
		lastTkn = nil
	} else {
		lastTkn = l.Tkns[len(l.Tkns)-1]
	}
	if lastTkn != nil {
		runes = l.Runes[RunesFromIdx(l.Runes, lastTkn.Val)+len(lastTkn.Val):]
	} else {
		runes = l.Runes
	}
	for len(runes) > 0 && unicode.IsSpace(runes[0]) {
		runes = runes[1:]
	}
	return
}

// Lexer.lexOpSp lexes the end of file.
func (l *Lexer) lexEOF() *Token {
	var runes = l.unlexRunes()
	if len(runes) == 0 {
		return NewToken(Eof, nil)
	}
	return nil
}

// Lexer.lexOpSp lexes an operator or separator and get a pointer to the token.
func (l *Lexer) lexOpSp() *Token {
	var runes = l.unlexRunes()
	
	// Judge the first rune is operator, separator or not.
	if strings.IndexRune("+-*/^();", runes[0]) >= 0 {
		return NewToken(map[rune]TknName{
			'+': OpAdd,
			'-': OpSub,
			'*': OpMlt,
			'/': OpDiv,
			'^': OpCrt,
			'(': SpLpr,
			')': SpRpr,
			';': SpSem,
		}[runes[0]], runes[:1])
	}
	return nil
}

// Lexer.lexIdent lexes an identifier and get a pointer to the token.
func (l *Lexer) lexIdent() *Token {
	var runes, tknLen = l.unlexRunes(), 0
	
	// The first rune must not be a number, operator or separator.
	if !unicode.IsDigit(runes[0]) && strings.IndexRune(
		"+-*/^();", runes[0]) < 0 {
		tknLen++
		// The last rune must end before a white, operator or separator.
		for tknLen < len(runes) && !unicode.IsSpace(runes[tknLen]) &&
			strings.IndexRune("+-*/^();", runes[tknLen]) < 0 {
			tknLen++
		}
		return NewToken(Ident, runes[:tknLen])
	}
	return nil
}

// Lexer.lexIt lexes an integer or float literal and get a pointer to the token.
// The rules will copy from C# version ≧ 7.2:
//   DIGIT  → Judge by isDigit(r, base) function defined inside.
//   SPACE  → Judge by unicode.IsSpace() function.
//   MINUS  → '-' { SPACE }
//   NNINT  → DIGIT { ( '_' | DIGIT ) } DIGIT
//   PREFIX → '0' ( 'x' | 'o' | 'b' )
//   IT_INT → [ MINUS ] [ PREFIX [ '_' ] ] NNINT
//   IT_FLT → [ MINUS ] ( NNINT '.' | NNINT '.' NNINT | '.' NNINT )
//   (Without scientific form, '+' sign and suffix support.)
func (l *Lexer) lexIt() *Token {
	var runes, hasPrefix = l.unlexRunes(), false
	var tknLen, minusLen, nnintLen, base = 0, 0, 0, 10
	
	// Function of deciding if rune is a digit or not in specified base.
	var isDigit = func(r rune, base int) bool {
		if r <= '9' {
			r = r - '0'
			return int(r) >= 0 && int(r) < base
		} else if []rune(strings.ToLower(string(r)))[0] >= 'a' {
			r = []rune(strings.ToLower(string(r)))[0] - 'a'
			return int(r) >= 0 && int(r) < base-11
		}
		return false
	}
	
	// Function of judging NNINT (non-negative integer).
	var judgeNnint = func(runes []rune, base int) (tknLen int) {
		if tknLen < len(runes) && isDigit(runes[tknLen], base) {
			tknLen++
			var contLowlnLen = 0
			for tknLen < len(runes) && (isDigit(
				runes[tknLen], base) || runes[tknLen] == '_') {
				// If the rune is '_', count continue length of '_'.
				if runes[tknLen] == '_' {
					if runes[tknLen-1] != '_' {
						contLowlnLen = 1
					} else {
						contLowlnLen++
					}
				}
				tknLen++
			}
			// If last rune is '_', exclude it.
			if runes[tknLen-1] == '_' {
				tknLen -= contLowlnLen
			}
		}
		return
	}
	
	// Judge [ MINUS ].
	if l.CanNumNeg && runes[tknLen] == '-' {
		minusLen++
		for unicode.IsSpace(runes[tknLen+minusLen]) {
			minusLen++
		}
	}
	tknLen = minusLen
	
	// Judge [ PREFIX [ '_' ] ].
	if tknLen+1 < len(runes) && runes[tknLen] == '0' && strings.IndexAny(
		string(runes[tknLen+1]), "xob") == 0 {
		if runes[tknLen+1] == 'x' {
			base = 16
		} else if runes[tknLen+1] == 'o' {
			base = 8
		} else if runes[tknLen+1] == 'b' {
			base = 2
		}
		tknLen += 2
		if runes[tknLen] == '_' {
			tknLen++
		}
		hasPrefix = true
	}
	
	// After [ MINUS ] [ PREFIX [ '_' ] ], judge '.'.
	if tknLen < len(runes) && runes[tknLen] == '.' {
		tknLen++
		if hasPrefix {
			// Fix [ MINUS ] PREFIX [ '_' ] '.' to [ MINUS ] '0' and return it.
			return NewToken(ItInt, runes[:minusLen+1])
		}
		// After [ MINUS ] '.', judge NNINT.
		if nnintLen = judgeNnint(runes[tknLen:], base); nnintLen > 0 {
			// return case IT_FLT → [ MINUS ] '.' NNINT.
			return NewToken(ItFlt, runes[:tknLen+nnintLen])
		} else {
			// [ MINUS ] '.' is nothing.
			return nil
		}
	}
	
	// After [ MINUS ] [ PREFIX [ '_' ] ], judge NNINT.
	if nnintLen = judgeNnint(runes[tknLen:], base); nnintLen > 0 {
		tknLen += nnintLen
		// After [ MINUS ] [ PREFIX [ '_' ] ] NNINT, Judge '.'.
		if tknLen < len(runes) && runes[tknLen] == '.' && !hasPrefix {
			// Return case IT_FLT → [ MINUS ] NNINT '.' [ NNINT ]
			tknLen += 1 + judgeNnint(runes[tknLen+1:], base)
			return NewToken(ItFlt, runes[:tknLen])
		} else {
			// Return case IT_INT → [ MINUS ] [ PREFIX [ '_' ] ] NNINT.
			return NewToken(ItInt, runes[:tknLen])
		}
	} else if hasPrefix {
		// Fix [ MINUS ] PREFIX [ '_' ] to [ MINUS ] '0' and return it.
		return NewToken(ItInt, runes[:minusLen+1])
	}
	
	return nil
}
