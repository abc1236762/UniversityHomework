package main

import (
	"flag"
	"image"
	"image/color"
	"image/gif"
	"image/jpeg"
	"image/png"
	"log"
	"math"
	"math/rand"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"

	"golang.org/x/image/bmp"
	"golang.org/x/image/tiff"
)

var (
	// 宣告程式的參數旗標，讓使用者可以決定輸入和輸出格式和雜訊比例。
	inImgPath = flag.String("i", "", `input image file's path`)
	outImgFmt = flag.String("f", "", `output image file's format [
	"bmp" | "gif" | "jpeg" | "png" | "tiff"
] (optional)`)
	noiseRate = flag.Float64("n", 0.01, `rate of salt and pepper noise (optional)`)
)

// 用來初始化程式的函式，預先檢查與處理參數旗標。
func init() {
	log.SetOutput(os.Stdout)
	rand.Seed(time.Now().UnixNano())
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
	// 將讀入的圖片轉換成灰階圖、加了雜訊後的圖與套用了濾鏡的圖。
	grayImg := imgToGrayImg(img)
	noisedImg := addSaltAndPepperNoise(grayImg)
	mean3By3Img := applyFilter(noisedImg, meanFiltering, 3, 3)
	mean5By5Img := applyFilter(noisedImg, meanFiltering, 5, 5)
	median3By3Img := applyFilter(noisedImg, medianFiltering, 3, 3)
	median5By5Img := applyFilter(noisedImg, medianFiltering, 5, 5)
	// 儲存圖片。
	saveImg("gray", grayImg)
	saveImg("noised", noisedImg)
	saveImg("mean3×3", mean3By3Img)
	saveImg("mean5×5", mean5By5Img)
	saveImg("median3×3", median3By3Img)
	saveImg("median5×5", median5By5Img)
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
	width, height := bounds.Max.X-bounds.Min.X, bounds.Max.Y-bounds.Min.Y
	// 建立一張與輸入的圖片相同尺寸的空圖片來存灰階圖。
	grayImg := image.NewGray(bounds)
	// 對每個每一個像素做疊代。
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			// 先取得指定像素的顏色轉換為8位元的灰階色並寫進新圖片。
			gray := color.GrayModel.Convert(img.At(x, y)).(color.Gray)
			grayImg.SetGray(x, y, gray)
		}
	}
	return grayImg
}

// 用來將一張灰階圖片增加椒鹽雜訊並輸出。
func addSaltAndPepperNoise(img *image.Gray) *image.Gray {
	bounds := img.Bounds()
	width, height := bounds.Max.X-bounds.Min.X, bounds.Max.Y-bounds.Min.Y
	size := width * height
	// 算好黑白兩色其中一個顏色會有幾個噪點。
	noisesOfOneColor := int(math.RoundToEven(float64(size) * *noiseRate / 2))
	noisesPos := make([]int, noisesOfOneColor*2)
	// 隨機產生出所有噪點在圖片上的座標並且是不重複的。
	for i := range noisesPos {
		for isDup := true; isDup; {
			noisesPos[i] = rand.Intn(size)
			isDup = false
			for j := 0; j < i; j++ {
				if noisesPos[j] == noisesPos[i] {
					isDup = true
					break
				}
			}
		}
	}
	// 將輸入的圖片複製出來拿來存加了噪點的圖。
	noisedImg := image.NewGray(bounds)
	copy(noisedImg.Pix, img.Pix)
	// 對每個要加入噪點的座標做疊代。
	for i, pos := range noisesPos {
		// 前半的座標填黑，後半的座標填白。
		var y8 uint8 = 0
		if i >= noisesOfOneColor {
			y8 = math.MaxUint8
		}
		// 將原本是一維的座標轉換成二維後，將噪點寫入至圖片。
		x, y := pos%width, pos/width
		noisedImg.SetGray(x, y, color.Gray{y8})
	}
	return noisedImg
}

// 取得圖片中會被用來進行濾波的區域，如果超出圖片邊界的話使用和OpenCV中的BORDER_REFLECT_101一樣的方式處理。
func getFilteringAreaOfImage(img *image.Gray, ox, oy, filterWidth, filterHeight int) [][]uint8 {
	bounds := img.Bounds()
	width, height := bounds.Max.X-bounds.Min.X, bounds.Max.Y-bounds.Min.Y
	// 先建立一個空的矩陣來存放從圖片中對於指定座標要和濾波器一樣尺寸的部份的色階。
	area := make([][]uint8, filterHeight)
	// 對每個濾波器的區域的座標做疊代，將座標對應的圖片上的座標的色階存入矩陣中，同時處理超出圖片範圍的狀況。
	for fy := range area {
		area[fy] = make([]uint8, filterWidth)
		for fx := range area[fy] {
			x, y := ox-(filterWidth-1)/2+fx, oy-(filterHeight-1)/2+fy
			if x < 0 {
				x = 0 - x
			} else if x >= width {
				x = (width-1)*2 - x
			}
			if y < 0 {
				y = 0 - y
			} else if y >= height {
				y = (height-1)*2 - y
			}
			area[fy][fx] = img.GrayAt(x, y).Y
		}
	}
	return area
}

// 進行均值濾波時的函式，會將區域中的每個色階值做平均。
func meanFiltering(area [][]uint8) uint8 {
	filterSize := len(area) * len(area[0])
	var result float64
	// 先累加色階值。
	for _, u := range area {
		for _, v := range u {
			result += float64(v)
		}
	}
	// 回傳奇進偶捨後的平均色階值。
	return uint8(math.RoundToEven(result / float64(filterSize)))
}

// 進行中值濾波時的函式，會將區域中的每個色階值排序後取中間值。
func medianFiltering(area [][]uint8) uint8 {
	filterSize := len(area) * len(area[0])
	// 先將包含了色階值的區域矩陣攤平並排列。
	var values []uint8
	for _, u := range area {
		values = append(values, u...)
	}
	sort.Slice(values, func(i, j int) bool { return values[i] < values[j] })
	// 回傳中間的值，如果是偶數個，則取中間兩個值平均後的值並做奇進偶捨後回傳。
	if filterSize%2 == 0 {
		return uint8(math.RoundToEven(float64(
			values[filterSize/2-1]+values[filterSize/2]) / 2))
	}
	return values[filterSize/2]
}

// 用來套用濾波器的函式，會將傳入的灰階圖片透過傳入的濾波器函式和其尺寸進行濾波並輸出。
func applyFilter(img *image.Gray, filterFunc func([][]uint8) uint8,
	filterWidth, filterHeight int) *image.Gray {
	bounds := img.Bounds()
	width, height := bounds.Max.X-bounds.Min.X, bounds.Max.Y-bounds.Min.Y
	// 建立一張與輸入的圖片相同尺寸的空圖片來存濾波後的結果。
	appliedImg := image.NewGray(bounds)
	// 對每個每一個像素做疊代。
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			// 先取得當前座標需要濾波的區域，套用濾波器後將結果的色階值寫進新圖片。
			area := getFilteringAreaOfImage(img, x, y, filterWidth, filterHeight)
			y8 := filterFunc(area)
			appliedImg.SetGray(x, y, color.Gray{y8})
		}
	}
	return appliedImg
}

// 當發生嚴重錯誤時紀錄錯誤訊息的函式。
func fatalWhenErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}
