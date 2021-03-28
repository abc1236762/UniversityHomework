package main

import (
	"fmt"
	"github.com/json-iterator/go/extra"
)

func init() {
	extra.SupportPrivateFields()
	extra.SetNamingStrategy(extra.LowerCaseWithUnderscores)
}

func main() {
	bc := NewBlockChain()
	bc.AddBlock([]byte("chain 1"))
	bc.AddBlock([]byte("chain 2"))
	bc.AddBlock([]byte("chain 3\n\"\tchain 3"))
	bc.AddBlock([]byte{51, 58, 12, 191})
	for height := 0; height <= bc.Height(); height++ {
		fmt.Println(bc.GetBlock(height))
	}
	bc.Export("ddd")
}
