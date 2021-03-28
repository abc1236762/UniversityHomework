package main

import (
	"crypto/sha256"
	"encoding/hex"
)

type Hash [sha256.Size]byte

func (h Hash) String() string {
	return hex.EncodeToString(h[:])
}
