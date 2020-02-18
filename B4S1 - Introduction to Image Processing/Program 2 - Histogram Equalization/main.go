package main

import (
	"encoding/base64"
	"flag"
	"image"
	"image/color"
	"image/gif"
	"image/jpeg"
	"image/png"
	"log"
	"math"
	"os"
	"path/filepath"
	"strings"

	"golang.org/x/image/bmp"
	"golang.org/x/image/tiff"
	"golang.org/x/image/webp"
)

// 宣告每一灰階像素有多少層級的顏色的常數。
const GrayLevels = 1 << 8

var (
	// 宣告程式的參數旗標，讓使用者可以決定輸入和輸出格式。
	inImgPath = flag.String("i", "", `input image file's path`)
	outImgFmt = flag.String("f", "", `output image file's format [
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

// 主要執行程式的函式，先讀入圖片，處理完後再儲存。
func main() {
	// 讀入圖片。
	img := openImg(*inImgPath)
	// 將讀入的圖片轉換成灰階圖與其直方圖、直方圖均衡化後的灰階圖與其直方圖。
	grayImg := imgToGrayImg(img)
	grayImgHist := drawHist(grayImg)
	equalizedImg := equalizeHist(grayImg)
	equalizedImgHist := drawHist(equalizedImg)
	// 儲存圖片。
	saveImg("gray", grayImg)
	saveImg("gray.hist", grayImgHist)
	saveImg("equalized", equalizedImg)
	saveImg("equalized.hist", equalizedImgHist)
}

// 用來開啟圖片的函式，可以支援多種圖片格式。
func openImg(imgPath string) image.Image {
	// 開啟圖片檔案。
	imgFile, err := os.Open(imgPath)
	fatalWhenErr(err)
	defer func() {
		fatalWhenErr(imgFile.Close())
	}()
	// 將開啟的圖片進行解碼，設置輸出格式，並回傳解碼後的圖片。
	img, imgFmt, err := image.Decode(imgFile)
	fatalWhenErr(err)
	if *outImgFmt == "" {
		*outImgFmt = imgFmt
	}
	return img
}

// 用來儲存圖片的函式，可以支援多種圖片格式。
func saveImg(postfix string, img image.Image) {
	// 處理圖片的輸出路徑。
	ext := "." + *outImgFmt
	if ext == ".jpeg" {
		ext = ".jpg"
	}
	inExtLen := len(filepath.Ext(*inImgPath))
	imgPath := (*inImgPath)[:len(*inImgPath)-inExtLen] + "_" + postfix + ext
	// 建立要寫入圖片的檔案。
	imgFile, err := os.Create(imgPath)
	fatalWhenErr(err)
	defer func() {
		fatalWhenErr(imgFile.Close())
	}()
	// 對應要輸出的格式，對圖片進行編碼並寫進檔案裡。
	switch strings.ToLower(*outImgFmt) {
	case "bmp":
		err = bmp.Encode(imgFile, img)
	case "gif":
		err = gif.Encode(imgFile, img, &gif.Options{NumColors: 256})
	case "jpeg", "jpg":
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

// 用來將任意圖片轉換成灰階圖片的函式。
func imgToGrayImg(img image.Image) *image.Gray {
	bounds := img.Bounds()
	// 建立一張空的灰階圖片，與輸入的圖片相同尺寸。
	grayImg := image.NewGray(img.Bounds())
	// 對每個每一個像素做疊代。
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			// 先取得指定像素的顏色（會得到16位元的RGB值），並轉換為8位元的RGB值。
			r16, g16, b16, _ := img.At(x, y).RGBA()
			r8, g8, b8 := uint8(r16>>8), uint8(g16>>8), uint8(b16>>8)
			// 套用公式轉成8位元的灰階值，並寫入至新圖片。
			y8 := uint8(0.299*float64(r8) + 0.587*float64(g8) + 0.114*float64(b8))
			grayImg.SetGray(x, y, color.Gray{y8})
		}
	}
	return grayImg
}

// 用來取得直方圖陣列的函式。
func getHist(img *image.Gray) []int {
	// 先初始化一個用來存各個灰階層級的數量的陣列。
	hist := make([]int, GrayLevels)
	// 疊代圖片中每個像素的灰階層級，並遞增數量。
	for _, y8 := range img.Pix {
		hist[y8]++
	}
	return hist
}

// 用來繪製直方圖的函式，會回傳輸入的灰階圖片的直方圖。
func drawHist(img *image.Gray) *image.Gray {
	// 準備繪製直方圖所需的模板圖片（WebP格式並以Base64紀錄）並解碼。
	histImgData := `data:image/webp;base64,UklGRvgAAABXRUJQVlA4TOwAAAAvF0FDAA8w//M///MfeHDbbJubsEKmv
	HFcE6+yPAPVVYTNkCtGcIU8AzmeXnL4ZKqjiOg/I7eRFLmlYbjN4gvQhCl9GxPIv26dhmnlskBmFUkr/d4wLkYzBFeDsoCLF
	YnkXOspmoP0udYsC9ieIumlxUiC9Llm6wU51xT3Tc7mAs3/hfsm2/pfuG8yZYGxVWilArEiCfbnWqxIJOdarxjNEF4ZhUQiV
	VD8mmOmwHftwG/QhQGiM0T+cYPm4lV7efMgAXIP7sYCbgPZBuwO3JPn5Pwy2TwlixcSIPOQ+KcRN87DfPemefZZ8w5NAA==`
	histImgData = strings.Split(strings.Join(strings.Fields(histImgData), ""), ",")[1]
	histWebp, err := webp.Decode(base64.NewDecoder(
		base64.StdEncoding, strings.NewReader(histImgData)))
	fatalWhenErr(err)
	// 宣告使用此模板圖片時，繪製直方圖的起始座標、最大範圍的像素點與對應值、直方條的不透明度與對應的灰階值。
	var (
		histImgPx, histImgPy = 22, 2
		histImgAh, histImgRh = 256, 2880
		histImgRy, histBarOp = float64(histImgAh) / float64(histImgRh), 0.5
		histBarY8            = uint8(math.RoundToEven(float64(GrayLevels-1) * histBarOp))
	)
	// 取得圖片的直方圖陣列後，找出最大值並保證不會超出此模板圖片能描繪的最大範圍。
	hist := getHist(img)
	histMax := 0
	for _, total := range hist {
		if histMax < total {
			histMax = total
		}
	}
	if histMax > histImgRh {
		log.Fatalf("drawing histogram only supported maximum %d points per color\n", histImgRh)
	}
	// 建立一張空的灰階圖片用來繪製直方圖，並先將模板圖片複製進去。
	histBounds := histWebp.Bounds()
	histImg := image.NewGray(histBounds)
	for y := histBounds.Min.Y; y < histBounds.Max.Y; y++ {
		for x := histBounds.Min.X; x < histBounds.Max.X; x++ {
			histImg.Set(x, y, histWebp.At(x, y))
		}
	}
	// 疊代直方圖陣列中，每個灰階層級與其像素點的數量。
	for y8, total := range hist {
		// 取得當前的總數須在直方圖上繪製條時需多少個像素點，因為算出的像素點不一定是整數，所以頂端的點可能會比較淺。
		pixels := float64(total) * histImgRy
		full := int(math.Floor(pixels))
		top := uint8(math.RoundToEven(GrayLevels * (1 - (pixels-float64(full))*histBarOp)))
		// 先對整數的像素點進行繪製。
		for y := histImgPy + histImgAh - 1; y >= histImgPy+histImgAh-full; y-- {
			histImg.SetGray(histImgPx+y8, y, color.Gray{histBarY8})
		}
		// 如果有不是整數的像素點也進行繪製。
		if top >= histBarY8 {
			histImg.SetGray(histImgPx+y8, histImgPy+histImgAh-1-full, color.Gray{top})
		}
	}
	return histImg
}

// 用來進行直方圖均衡化的函式，輸入任一灰階圖片，會回傳轉換後的灰階圖片。
func equalizeHist(img *image.Gray) *image.Gray {
	// 取得直方圖陣列後，製作累積分佈陣列，並取得累積分佈的最大與最小值。
	hist := getHist(img)
	cd := make([]int, GrayLevels)
	for i := range cd {
		if i != 0 {
			cd[i] = cd[i-1] + hist[i]
		} else {
			cd[i] = hist[i]
		}
	}
	cdMin, cdMax := cd[0], cd[len(cd)-1]
	// 進行直方圖均衡化，製作紀錄每一個灰階層級在均衡化之後的灰階層級的陣列。
	h := make([]uint8, GrayLevels)
	for y8 := range h {
		h[y8] = uint8(math.RoundToEven(float64(cd[y8]-cdMin) /
			float64(cdMax-cdMin) * float64(GrayLevels-1)))
	}
	// 建立一張空的灰階圖片，與輸入的圖片相同尺寸，並將原本的圖片每一像素的灰階層級做直方圖均衡化並寫入至新圖片。
	equalizedImg := image.NewGray(img.Bounds())
	for i := range equalizedImg.Pix {
		equalizedImg.Pix[i] = h[img.Pix[i]]
	}
	return equalizedImg
}

// 當發生嚴重錯誤時紀錄錯誤訊息的函式。
func fatalWhenErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}
