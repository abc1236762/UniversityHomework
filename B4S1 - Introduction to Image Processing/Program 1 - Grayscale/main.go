package main

import (
	"flag"
	"image"
	"image/color"
	"image/gif"
	"image/jpeg"
	"image/png"
	"log"
	"os"
	"path/filepath"
	"strings"

	"golang.org/x/image/bmp"
	"golang.org/x/image/tiff"
	_ "golang.org/x/image/webp"
)

var (
	// 宣告程式的參數旗標，讓使用者可以決定輸入和輸出路徑及格式。
	inImgPath  = flag.String("i", "", `input image file's path`)
	outImgPath = flag.String("o", "", `output image file's path (optional)`)
	outImgFmt  = flag.String("f", "", `output image file's format [
	"bmp" | "gif" | "jpeg" | "png" | "tiff"
] (optional)`)
)

// 用來初始化程式的函式，預先檢查與處理參數旗標。
func init() {
	log.SetOutput(os.Stdout)
	flag.Parse()
	if *inImgPath == "" {
		log.Fatalln("required flag -i and its value")
	}
	*outImgFmt = strings.ToLower(*outImgFmt)
}

// 主要執行程式的函式，先讀入圖片，轉成灰階後在儲存。
func main() {
	// 讀入圖片。
	inImg := openImg(*inImgPath)
	bounds := inImg.Bounds()
	// 建立一張空的灰階圖片，與讀入的圖片相同尺寸。
	outImg := image.NewGray(bounds)
	// 對每個每一個像素迭代。
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			// 先取得指定像素的顏色（會得到16位元的RGB值），並轉換為8位元的RGB值。
			r16, g16, b16, _ := inImg.At(x, y).RGBA()
			r8, g8, b8 := uint8(r16 >> 8), uint8(g16 >> 8), uint8(b16 >> 8)
			// 套用公式轉成8位元的灰階值，並寫入至新圖片。
			y8 := uint8(0.299 * float64(r8) + 0.587 * float64(g8) + 0.114 * float64(b8))
			outImg.SetGray(x, y, color.Gray{y8})
		}
	}
	// 儲存處理完的灰階圖片。
	saveImg(*outImgPath, outImg)
}

// 用來開啟圖片的函式，可以支援多種圖片格式。
func openImg(imgPath string) image.Image {
	// 開啟圖片檔案。
	imgFile, err := os.Open(imgPath)
	fatalWhenErr(err)
	defer func() {
		fatalWhenErr(imgFile.Close())
	}()
	// 將開啟的圖片進行解碼，設置輸出路徑，並回傳解碼後的圖片。
	img, imgFmt, err := image.Decode(imgFile)
	fatalWhenErr(err)
	if *outImgFmt == "" {
		*outImgFmt = imgFmt
	}
	if *outImgPath == "" {
		ext := "." + *outImgFmt
		if ext == ".jpeg" {
			ext = ".jpg"
		}
		inExtLen := len(filepath.Ext(*inImgPath))
		*outImgPath = (*inImgPath)[:len(*inImgPath)-inExtLen] + "_result" + ext
	}
	return img
}

// 用來儲存圖片的函式，可以支援多種圖片格式。
func saveImg(imgPath string, img image.Image) {
	// 建立要寫入圖片的檔案。
	imgFile, err := os.Create(imgPath)
	fatalWhenErr(err)
	defer func() {
		fatalWhenErr(imgFile.Close())
	}()
	// 對應要輸出的格式，對圖片進行編碼並寫進檔案裡。
	switch *outImgFmt {
	case "bmp":
		err = bmp.Encode(imgFile, img)
	case "gif":
		err = gif.Encode(imgFile, img, &gif.Options{NumColors: 256})
	case "jpeg":
		err = jpeg.Encode(imgFile, img, &jpeg.Options{Quality: 100})
	case "png":
		err = png.Encode(imgFile, img)
	case "tiff":
		err = tiff.Encode(imgFile, img, &tiff.Options{Compression: tiff.Deflate})
	default:
		log.Fatalf("not supported to output image format \"%s\"\n", *outImgFmt)
	}
	fatalWhenErr(err)
}

// 當發生嚴重錯誤時紀錄錯誤訊息的函式。
func fatalWhenErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}
