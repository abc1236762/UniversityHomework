package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"encoding/binary"
	"fmt"
	"strconv"
	"time"
)

type Block struct {
	height     int
	parentHash Hash
	time       int64
	data       []byte
	hash       Hash
}

func NewBlock(data []byte, parentHash Hash, height int) *Block {
	b := new(Block)
	b.height = height
	b.parentHash = parentHash
	b.time = time.Now().Unix()
	b.data = make([]byte, len(data))
	copy(b.data, data)
	b.hash = b.calculateHash()
	return b
}

func genesisBlock() *Block {
	b := new(Block)
	b.height = 0
	b.time = time.Now().Unix()
	b.data = []byte("genesis block")
	b.hash = b.calculateHash()
	return b
}

func (b *Block) Height() int {
	return b.height
}

func (b *Block) ParentHash() Hash {
	return b.parentHash
}

func (b *Block) Time() time.Time {
	return time.Unix(b.time, 0)
}

func (b *Block) Data() []byte {
	return b.data
}

func (b *Block) Hash() Hash {
	return b.hash
}

func (b *Block) String() string {
	str := fmt.Sprintf("Height %3d\n", b.Height())
	str += fmt.Sprintf("- Parent hash  : %v\n", b.ParentHash())
	str += fmt.Sprintf("- Time         : %v\n", b.Time())
	str += fmt.Sprintf("- Data (quoted): %s\n", strconv.Quote(string(b.Data())))
	str += fmt.Sprintf("- Data (base64): %s\n", base64.StdEncoding.EncodeToString(b.Data()))
	str += fmt.Sprintf("- Hash         : %v", b.Hash())
	return str
}

func (b *Block) calculateHash() Hash {
	timeBytes := make([]byte, 8)
	binary.LittleEndian.PutUint64(timeBytes, uint64(b.time))
	bytes := bytes.Join([][]byte{b.parentHash[:], timeBytes, b.data}, []byte{})
	return sha256.Sum256(bytes)
}
