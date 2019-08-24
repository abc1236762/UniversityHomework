# A recursive descent parser including a lexical analyzer
實作包含詞法分析器的語法分析器

GNU General Public License v3.0

## Usage
The files that input or output should or will encoded by UTF-8 without bom,
and must use `'\n'` (Unix LF) as newline character.

Every code in the input text file should use a blank line to separate, like:
```
x ^ (y+1) - x/2.5 + z;
sum + total * 10;

3 + x*y);
```
There are two group codes will be parsed.

### Command-line flags

| Flag | Usage |
| - | - |
| `-i <path>` | The path of a input text file including many code groups. |
| `-o <path>` | The path of a output text file including the parsing result. |
| `-n` | Use it to make the parser allow numbers be negative. |
| `-h` | Show the help of command-line flags. |

Default of path of input file is `./input.txt`, output’s is `./result.txt`.

## Parsing rules
```
<exprs> → <expr> ';' { <expr> ';' }
<expr>  → <term> { ( '+' | '-' ) <term> }
<term>  → <fctr> { ( '*' | '/' ) <fctr> }
<fctr>  → <exp>  { '^' <exp> }
<exp>   → IDENT | IT_INT | IT_FLT | '(' <expr> ')'
```
IDENT is identifier, IT_INT and IT_FLT are integer and float literal.

IT_INT and IT_FLT in this project follow the rules in C# version ≧ 7.2 
without scientific form, '+' sign and suffix support:
```
DIGIT  → Judge by isDigit(r, base) function defined in Lexer.lexIt().
SPACE  → Judge by unicode.IsSpace() function.
MINUS  → '-' { SPACE }
NNINT  → DIGIT { ( '_' | DIGIT ) } DIGIT
PREFIX → '0' ( 'x' | 'o' | 'b' )
IT_INT → [ MINUS ] [ PREFIX [ '_' ] ] NNINT
IT_FLT → [ MINUS ] ( NNINT '.' | NNINT '.' NNINT | '.' NNINT )
```

IDENT allows any characters excluding space characters, listed operators
and separators, but the first character of IDENT can not be a ten’s
digit. The lexing order will be EOF → IT_INT/IT_FLT → OP/SP → IDENT, but
when the last token is ')', IDENT or IT_INT/IT_FLT, it will be EOF → OP/SP
→ IT_INT/IT_FLT → IDENT. OP/SP is usually next to IT_INT/IT_FLT and IDENT.
