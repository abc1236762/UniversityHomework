package main

import (
	"github.com/json-iterator/go"
	"fmt"
)

type BlockChain struct {
	blocks []*Block
}

func NewBlockChain() *BlockChain {
	return &BlockChain{[]*Block{genesisBlock()}}
}

func LoadBlockChain() (*BlockChain, error) {
	return nil, nil
}

func (bc *BlockChain) AddBlock(data []byte) {
	height := len(bc.blocks)
	parentHash := bc.blocks[height-1].hash
	block := NewBlock(data, parentHash, height)
	bc.blocks = append(bc.blocks, block)
}

func (bc *BlockChain) GetBlock(height int) *Block {
	return bc.blocks[height]
}

func (bc *BlockChain) Height() int {
	return len(bc.blocks) - 1
}

func (bc *BlockChain) Export(path string) error {
	data, err := jsoniter.Marshal(bc)
	if err != nil {
		return err
	}
	fmt.Println(string(data))
	return nil
}
