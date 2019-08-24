package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func main() {
	srcFilename, dstFilename := os.Args[1], os.Args[2]
	
	var lines []string
	if content, err := ioutil.ReadFile(srcFilename); err != nil {
		panic(err)
	} else {
		contentStr := string(content[:])
		contentStr = strings.Replace(contentStr, "\r\n", "\n", -1)
		contentStr = strings.Replace(contentStr, "\r", "\n", -1)
		lines = strings.Split(contentStr, "\n")
	}
	
	statToNextTable := make(map[int][2]string)
	
	rulesFrom, rulesTo := rulesSectionRange(lines)
	for i := rulesFrom; i <= rulesTo; i++ {
		if !isLineStatNext(lines, i) {
			continue
		}
		
		srcStatLine := strings.TrimSpace(lines[findSrcStatLine(lines, i)])
		distStatLine := strings.TrimSpace(lines[i])
		distStatLine = strings.TrimPrefix(distStatLine, ":")
		distStatLine = strings.TrimPrefix(distStatLine, "|")
		distStatLine = strings.TrimSpace(distStatLine)
		if distStatLine == "" {
			distStatLine = "(null)"
		}
		statToNextTable[i] = [2]string{srcStatLine, distStatLine}
	}
	
	genStatMsg(lines, statToNextTable)
	
	result := []byte(strings.Join(lines, "\n"))
	if err := ioutil.WriteFile(dstFilename, result, 0666); err != nil {
		panic(err)
	}
}

func rulesSectionRange(lines []string) (from, to int) {
	from, to = -1, -1
	for i, line := range lines {
		if line == "%%" {
			if from < 0 {
				from = i + 1
			} else {
				to = i - 1
			}
		}
		if from >= 0 && to >= 0 {
			return
		}
	}
	panic("msg_maker: cannot find rules section")
	return
}

func isLineStatNext(lines []string, i int) bool {
	lineRunes := []rune(strings.TrimSpace(lines[i]))
	return len(lineRunes) >= 1 && (lineRunes[0] == ':' || lineRunes[0] == '|')
}

func findSrcStatLine(lines []string, i int) int {
	for j := i - 1; j >= 0; j-- {
		line := strings.TrimSpace(lines[j])
		if !isLineStatNext(lines, j) && line != ";" && line != "" {
			return j
		}
	}
	panic(fmt.Errorf("msg_maker: cannot find source statment line of %d", i))
	return -1
}

func genStatMsg(lines []string, statToNextTable map[int][2]string) {
	maxSrcStatLen := 0
	for _, s := range statToNextTable {
		if srcStatLen := len([]rune(s[0])); srcStatLen > maxSrcStatLen {
			maxSrcStatLen = srcStatLen
		}
	}
	
	for i, s := range statToNextTable {
		if len([]rune(lines[i])) <= 80-1 {
			lines[i] = fmt.Sprintf("%-79s", lines[i])
		}
		s[0] = fmt.Sprintf("%-"+strconv.Itoa(maxSrcStatLen)+"s", s[0])
		lines[i] += fmt.Sprintf(" { printf(\"%s -> %s\\n\"); }", s[0], s[1])
	}
}
