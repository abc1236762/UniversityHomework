// Parser Implementation Homework
// Written by 410521209 林鈺錦
// GNU General Public License v3.0
//
// This project is written by Go Programming Language.
// Before reviewing it, there are some special point in Go you need to realize:
//   1. About passing parameters: In Go, there are not any types passing by
//   reference, only passing by value and passing by pointer. All types
//   in Go passing by value, include array ([<num>]<type>), struct and
//   string. Map (map[<type>]<type>) and slice ([]<type>) are reference
//   types but also passing by value. All types in Go can also passing
//   by pointer with '&' prefix like C/C++.
//   2. About enum type: Go uses defining a new type form the number type and
//   defining a list of constants with that type to make an enum type.
//   3. About string and rune type: String type in Go is generally encoded
//   by UTF-8. If using <string>[<num>] to try to get a element in a string,
//   it will return the value of index of <num> in the byte array from
//   the string. Before getting a character in a string, convert string
//   to rune (means unicode character) array like []rune(<string>) first.
//   4. About slice type: Slice type in Go a reference to a contiguous segment
//   of an array. It save the pointer that point to the assigned position of an
//   array, length of segment and its capacity. Using <array>[:] to reference
//   all of <array>, using <array>[<num1>:<num2>] to reference <array> from
//   index <num1> until index <num2> or <array>[<num1>:] and <array>[:<num2>].
//   Also using `<slice> = append(<slice>, <sth>)` to add <sth> to <slice>.
//   5. About class: Go is not an OOP language, but it can use a struct
//   and define some functions inside the struct to simulate a class.
//   A function in a struct is public if first alphabet of its name is
//   upper case, and is private if first alphabet of it is lower case.
//
// This project uses the following parsing rules :
//   <exprs> → <expr> ';' { <expr> ';' }
//   <expr>  → <term> { ( '+' | '-' ) <term> }
//   <term>  → <fctr> { ( '*' | '/' ) <fctr> }
//   <fctr>  → <exp>  { '^' <exp> }
//   <exp>    → IDENT | IT_INT | IT_FLT | '(' <expr> ')'
//   IDENT is identifier, IT_INT and IT_FLT are integer and float literal.
//   IT_INT and IT_FLT in this project follow the rules in C# version ≧ 7.2:
//     DIGIT  → Judge by isDigit(r, base) function defined in Lexer.lexIt().
//     SPACE  → Judge by unicode.IsSpace() function.
//     MINUS  → '-' { SPACE }
//     NNINT  → DIGIT { ( '_' | DIGIT ) } DIGIT
//     PREFIX → '0' ( 'x' | 'o' | 'b' )
//     IT_INT → [ MINUS ] [ PREFIX [ '_' ] ] NNINT
//     IT_FLT → [ MINUS ] ( NNINT '.' | NNINT '.' NNINT | '.' NNINT )
//     (Without scientific form, '+' sign and suffix support.)
//   IDENT allows any characters excluding space characters, listed operators
//   and separators, but the first character of IDENT can not be a ten’s
//   digit. The lexing order will be EOF → IT_INT/IT_FLT → OP/SP → IDENT,but
//   when the last token is ')', IDENT or IT_INT/IT_FLT, it will be EOF → OP/SP
//   → IT_INT/IT_FLT → IDENT. OP/SP is usually next to IT_INT/IT_FLT and IDENT.
//
// The files that input or output should or will encoded by UTF-8 without bom.
// Every code in the input text file should use a blank line to separate, like:
// > x ^ (y+1) - x/2.5 + z;
// > sum + total * 10;
// >
// > 3 + x*y);
// There are two group codes will be parsed. (`> ` will not exist in the file.)
//
// Command-line flags:
//   Flag        Usage
// -i <path>   The path of a input text file including many code groups.
// -o <path>   The path of a output text file including the parsing result.
// -n          Use it to make the parser allow numbers be negative.
// -h          Show the help of command-line flags.
// Default of path of input file is "./input.txt", output’s is "./result.txt".

package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
	"unsafe"
)

func main() {
	var err error
	var textByte []byte
	var outputFile, logFile *os.File
	var inputPath, outputPath, canNumNeg = "./input.txt", "./result.txt", false
	
	// Set and parse the flags.
	flag.StringVar(&inputPath, "i", inputPath,
		"The path of a input text file including many code groups.\n"+
			"The file should encoded by UTF-8 without bom.")
	flag.StringVar(&outputPath, "o", outputPath,
		"The path of a output text file including the parsing result.\n"+
			"The file will encoded by UTF-8 without bom.")
	flag.BoolVar(&canNumNeg, "n", canNumNeg,
		"Use it to make the parser allow numbers be negative.")
	flag.Parse()
	
	// Create files for output and logs and read the file to byte array.
	if logFile, err = os.OpenFile("errors.log",
		os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644); err != nil {
		log.Fatal(err)
	}
	log.SetOutput(logFile)
	if textByte, err = ioutil.ReadFile(inputPath); err != nil {
		log.Fatal(err)
	}
	if outputFile, err = os.Create(outputPath); err != nil {
		log.Fatal(err)
	}
	var writer = bufio.NewWriter(outputFile)
	
	// Split different codes to string array and begin parsing it.
	for i, code := range strings.Split(string(textByte), "\n\n") {
		if _, err = writer.WriteString(fmt.Sprintf(
			"* Code %d ```\n%s\n``` has\n", i+1, code)); err != nil {
			log.Fatal(err)
		}
		var psr = NewParser(code, canNumNeg)
		psr.Lxr.Lex()
		if _, err = writer.WriteString(psr.Lxr.SprintTkns()); err != nil {
			log.Fatal(err)
		}
		psr.Parse()
		writer.WriteString(psr.SprintTree())
		if len(psr.Errs) == 0 {
			writer.WriteString("The parsing is successful.\n")
		} else {
			writer.WriteString(fmt.Sprintf("The parsing is "+
				"unsuccessful with %d error(s).\n—Errors:\n", len(psr.Errs)))
			for _, err := range psr.Errs {
				writer.WriteString(err.Error())
			}
		}
		if _, err = writer.WriteString("\n"); err != nil {
			log.Fatal(err)
		}
	}
	
	// Flush the writer and close files.
	if err = writer.Flush(); err != nil {
		log.Fatal(err)
	}
	if err = outputFile.Close(); err != nil {
		log.Fatal(err)
	}
	if err = logFile.Close(); err != nil {
		log.Fatal(err)
	}
}

// RunesFromIdx returns start index of runes from the source runes.
func RunesFromIdx(srcRunes, runes []rune) int {
	var srcRunePtr = uintptr(unsafe.Pointer(&srcRunes[0]))
	var runePtr = uintptr(unsafe.Pointer(&runes[0]))
	return int((runePtr - srcRunePtr) / unsafe.Sizeof(rune(0)))
}

// UnescapeStr returns an unescaped string.
func UnescapeStr(s string) string {
	return strings.NewReplacer("\a", `\a`, "\b", `\b`, "\f", `\f`, "\n", `\n`,
		"\r", `\r`, "\t", `\t`, "\v", `\v`, "\\", `\\`, "\"", `\"`).Replace(s)
}
