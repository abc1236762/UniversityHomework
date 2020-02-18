package main

import (
	"errors"
	"flag"
	"fmt"
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
	"strings"
	"time"

	"golang.org/x/image/bmp"
	"golang.org/x/image/tiff"
)

// 實作一個簡單的雙經度浮點數矩陣的資料結構。
type F64Mat struct {
	mat  [][]float64
	W, H int
}

// 用來生成一個雙經度浮點數矩陣。
func MakeF64Mat(matW, matH int) F64Mat {
	mat := make([][]float64, matH)
	for i := range mat {
		mat[i] = make([]float64, matW)
	}
	return F64Mat{mat, matW, matH}
}

// 用來設定矩陣中的值。
func (m *F64Mat) Set(x, y int, val float64) {
	m.mat[y][x] = val
}

// 用來取得矩陣中的值。
func (m *F64Mat) Get(x, y int) float64 {
	return m.mat[y][x]
}

// 用來複製矩陣中一部分的區域到當前矩陣中。
func (m *F64Mat) CopyFrom(src F64Mat, x1, y1, srcX1, srcY1, rangeW, rangeH int) {
	for y := 0; y < rangeH; y++ {
		for x := 0; x < rangeW; x++ {
			m.mat[y1+y][x1+x] = src.mat[srcY1+y][srcX1+x]
		}
	}
}

// 用來輸出兩個矩陣的值的差異絕對值。
func (m *F64Mat) AbsDiff(mat F64Mat) F64Mat {
	if m.W != mat.W || m.H != mat.H {
		fatalWhenErr(errors.New("m's size does not match mat's size"))
	}
	diffMat := MakeF64Mat(m.W, m.H)
	for y := 0; y < m.H; y++ {
		for x := 0; x < m.W; x++ {
			diffMat.mat[y][x] = math.Abs(m.mat[y][x] - mat.mat[y][x])
		}
	}
	return diffMat
}

var (
	// 宣告程式的參數旗標，讓使用者可以決定輸入和輸出格式。
	inImgPath = flag.String("i", "", `input image file's path`)
	outImgFmt = flag.String("f", "", `output image file's format [
	"bmp" | "gif" | "jpeg" | "png" | "tiff"
] (optional)`)
)

// 空矩陣，用來忽略參數，但需要與量化表相同尺寸。
var emptyTable = F64Mat{
	[][]float64{
		{0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0},
	}, 8, 8,
}

// 量化表。
var quantizationTable = F64Mat{
	[][]float64{
		{16, 11, 10, 16, 24, 40, 51, 61},
		{12, 12, 14, 19, 26, 58, 60, 55},
		{14, 13, 16, 24, 40, 57, 69, 56},
		{14, 17, 22, 29, 51, 87, 80, 62},
		{18, 22, 37, 56, 68, 109, 103, 77},
		{24, 35, 55, 64, 81, 104, 113, 92},
		{49, 64, 78, 87, 103, 121, 120, 101},
		{72, 92, 95, 98, 112, 100, 103, 99},
	}, 8, 8,
}

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
	// 讀入圖片、取得圖片的長寬。
	img := openImg(*inImgPath)
	bounds := img.Bounds()
	imgW, imgH := bounds.Max.X-bounds.Min.X, bounds.Max.Y-bounds.Min.Y
	// 將讀入的圖片轉換成灰階圖並儲存，然後轉成長寬能夠與量化表的尺寸整除的雙經度浮點數矩陣。
	grayImg := imgToGrayImg(img)
	saveImg("gray", grayImg)
	mat := grayImgToF64MatWithDivisibleSize(grayImg, quantizationTable.W, quantizationTable.H)
	// 執行DCT處理，不須代入表（代入空表），輸出成圖片時必須把色階適應至0至255。
	dcted := processWholeMat(mat, emptyTable, false, discreteCosineTransform)
	dctedImg := f64MatToGrayImgWithOriginalSize(dcted, imgW, imgH, true)
	saveImg("dct", dctedImg)
	// 執行量化處理，須代入量化表，輸出成圖片時必須把色階適應至0至255。
	qnted := processWholeMat(dcted, quantizationTable, false, quantization)
	qntedImg := f64MatToGrayImgWithOriginalSize(qnted, imgW, imgH, true)
	saveImg("qnt", qntedImg)
	// 執行反量化處理，須代入量化表，輸出成圖片時必須把色階適應至0至255。
	iqnted := processWholeMat(qnted, quantizationTable, true, quantization)
	iqntedImg := f64MatToGrayImgWithOriginalSize(iqnted, imgW, imgH, true)
	saveImg("iqnt", iqntedImg)
	// 執行IDCT處理，不須代入表（代入空表），輸出成圖片時不須把色階適應至0至255（如有超出應當修正回極限）。
	idcted := processWholeMat(iqnted, emptyTable, true, discreteCosineTransform)
	idctedImg := f64MatToGrayImgWithOriginalSize(idcted, imgW, imgH, false)
	saveImg("idct", idctedImg)
	// 將IDCT處理後的矩陣與原本的相減並做絕對值，得到兩者的差異，並輸出成圖片，輸出成圖片時必須把色階適應至0至255。
	diffMat := idcted.AbsDiff(mat)
	diffImg := f64MatToGrayImgWithOriginalSize(diffMat, imgW, imgH, true)
	saveImg("diff", diffImg)
	// 計算PSNR並印出。
	psnr := getPeakSignalToNoiseRatioOfGrayImg(grayImg, idctedImg)
	fmt.Println("PSNR:", psnr)
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
	imgW, imgH := bounds.Max.X-bounds.Min.X, bounds.Max.Y-bounds.Min.Y
	// 建立一張與輸入的圖片相同尺寸的空圖片來存灰階圖。
	grayImg := image.NewGray(bounds)
	// 對每個每一個像素做疊代。
	for y := 0; y < imgH; y++ {
		for x := 0; x < imgW; x++ {
			// 先取得指定像素的顏色轉換為8位元的灰階色並寫進新圖片。
			gray := color.GrayModel.Convert(img.At(x, y)).(color.Gray)
			grayImg.SetGray(x, y, gray)
		}
	}
	return grayImg
}

// 將灰階圖片轉成雙經度浮點數的矩陣，並且矩陣的長寬可以分別整除某個數。
func grayImgToF64MatWithDivisibleSize(img *image.Gray, unitW, unitH int) F64Mat {
	bounds := img.Bounds()
	imgW, imgH := bounds.Max.X-bounds.Min.X, bounds.Max.Y-bounds.Min.Y
	matW, matH := imgW, imgH
	// 如果原本圖片的長寬不能被某個數整除，就延伸至可以整除的大小。
	if imgW%unitW != 0 {
		matW += unitW - (imgW - imgW/unitW*unitW)
	}
	if imgH%unitH != 0 {
		matH += unitH - (imgH - imgH/unitH*unitH)
	}
	// 建立一個空的矩陣，並把圖片中每個像素的灰階值轉成浮點數後放進矩陣中。
	mat := MakeF64Mat(matW, matH)
	for y := 0; y < imgH; y++ {
		for x := 0; x < imgW; x++ {
			mat.Set(x, y, float64(img.GrayAt(x, y).Y))
		}
	}
	return mat
}

// 將雙經度浮點數的矩陣轉換為圖片，並與輸入的圖片尺寸相符，且要考慮是否要改變色階的範圍至0到255。
func f64MatToGrayImgWithOriginalSize(mat F64Mat, imgW, imgH int, isFitRange bool) *image.Gray {
	max, min := math.SmallestNonzeroFloat64, math.MaxFloat64
	// 如果要改變色階的範圍至0到255，就要先取得當前矩陣的最大值和最小值。
	if isFitRange {
		for y := 0; y < imgH; y++ {
			for x := 0; x < imgW; x++ {
				val := mat.Get(x, y)
				if val > max {
					max = val
				}
				if val < min {
					min = val
				}
			}
		}
		// fmt.Println(max, min)
	}
	// 建立一個空的圖片，並把矩陣中的每個值轉成8位元的非負整數並放入圖片中。
	img := image.NewGray(image.Rect(0, 0, imgW, imgH))
	for y := 0; y < imgH; y++ {
		for x := 0; x < imgW; x++ {
			val := mat.Get(x, y)
			// 如果要改變色階的範圍至0到255，就將值重新計算，否則大於255就修正回255，小於0就修正回0。
			if isFitRange {
				val = (val - min) / (max - min) * math.MaxUint8
			} else {
				if val > math.MaxUint8 {
					val = math.MaxUint8
				} else if val < 0 {
					val = 0
				}
			}
			img.SetGray(x, y, color.Gray{uint8(math.RoundToEven(val))})
		}
	}
	return img
}

// 代入用來處理每個區塊的函式來處理整個矩陣。
func processWholeMat(src, arg F64Mat, isInverse bool, p func(F64Mat, F64Mat, bool) F64Mat) F64Mat {
	if src.W%arg.W != 0 || src.H%arg.W != 0 {
		fatalWhenErr(errors.New("src's size is not divisible with arg's size"))
	}
	// 先建立一個空的矩陣用來回傳結果，並每個區塊作疊代。
	result := MakeF64Mat(src.W, src.H)
	for y := 0; y < src.H; y += arg.H {
		for x := 0; x < src.H; x += arg.W {
			// 把當前矩陣中的區塊複製出來。
			block := MakeF64Mat(arg.W, arg.H)
			block.CopyFrom(src, 0, 0, x, y, arg.W, arg.H)
			// 將複製出來的區塊經過處理後，複製回存結果的矩陣。
			processed := p(block, arg, isInverse)
			result.CopyFrom(processed, x, y, 0, 0, arg.W, arg.H)
		}
	}
	return result
}

// 處理DCT或IDCT，須符合傳入processWholeMat函式的p參數格式，但只需要傳入一個矩陣，因此另一個要忽略。
// 參考：https://www.mathworks.com/help/images/discrete-cosine-transform.html
func discreteCosineTransform(src, _ F64Mat, isInverse bool) F64Mat {
	nX, nY, nXF, nYF := src.W, src.H, float64(src.W), float64(src.H)
	// C(p,q)=cos((π×(q_x×2+1)×p_x)/(N_x×2))×cos((π×(q_y×2+1)×p_y)/(N_y×2))
	c := func(p, q image.Point) float64 {
		pXF, pYF := float64(p.X), float64(p.Y)
		qXF, qYF := float64(q.X), float64(q.Y)
		return math.Cos((math.Pi*(qXF*2+1)*pXF)/(nXF*2)) * math.Cos((math.Pi*(qYF*2+1)*pYF)/(nYF*2))
	}
	// d_x(p_x=0)=(1/√N_x), d_x(p_x>0)=√(2/N_x) => d_x(p_x>0)=d_x(p_x=0)×√2
	// d_y(p_y=0)=(1/√N_y), d_y(p_y>0)=√(2/N_y) => d_y(p_y>0)=d_y(p_y=0)×√2
	// D(p)=d_x(p_x)×d_y(p_y)
	d := func(p image.Point) float64 {
		dX, dY := 1/math.Sqrt(nXF), 1/math.Sqrt(nYF)
		if p.X > 0 {
			dX *= math.Sqrt(2)
		}
		if p.Y > 0 {
			dY *= math.Sqrt(2)
		}
		return dX * dY
	}
	// G(p)=input[p_y][p_x]
	g := func(p image.Point) float64 {
		return src.Get(p.X, p.Y)
	}
	// O(i)=∑{j:x=0~N_x-1,y=0~N_y-1}(D(i)×G(j)×C(i,j)) (DCT)
	// O(i)=∑{j:x=0~N_x-1,y=0~N_y-1}(D(j)×G(j)×C(j,i)) (IDCT)
	o := func(i image.Point) float64 {
		sum := 0.0
		for y := 0; y < nY; y++ {
			for x := 0; x < nX; x++ {
				j := image.Point{x, y}
				if !isInverse {
					sum += d(i) * g(j) * c(i, j)
				} else {
					sum += d(j) * g(j) * c(j, i)
				}
			}
		}
		return sum
	}
	// 先建立一個空的矩陣用來回傳單一區塊做DCT或IDCT的結果，並疊代每個位置進行DCT或IDCT。
	result := MakeF64Mat(nX, nY)
	for y := 0; y < nY; y++ {
		for x := 0; x < nX; x++ {
			i := image.Point{x, y}
			result.Set(x, y, o(i))
		}
	}
	return result
}

// 處理量化或反量化，須符合傳入processWholeMat函式的p參數格式。
func quantization(src F64Mat, table F64Mat, isInverse bool) F64Mat {
	if src.W != table.W || src.H != table.H {
		fatalWhenErr(errors.New("src's size does not match table's size"))
	}
	// 先建立一個空的矩陣用來回傳單一區塊做量化或反量化的結果，並疊代每個位置進行量化或反量化。
	result := MakeF64Mat(src.W, src.H)
	for y := 0; y < src.H; y++ {
		for x := 0; x < src.W; x++ {
			if !isInverse {
				result.Set(x, y, math.RoundToEven(src.Get(x, y)/table.Get(x, y)))
			} else {
				result.Set(x, y, src.Get(x, y)*table.Get(x, y))
			}
		}
	}
	return result
}

// 用來取得兩灰階圖片間的PSNR值。參考：https://www.mathworks.com/help/vision/ref/psnr.html
func getPeakSignalToNoiseRatioOfGrayImg(
	img1 *image.Gray, img2 *image.Gray) float64 {
	bounds := img1.Bounds()
	if bounds != img2.Bounds() {
		fatalWhenErr(errors.New("img1's size does not match img2's size"))
	}
	imgW, imgH := bounds.Max.X-bounds.Min.X, bounds.Max.Y-bounds.Min.Y
	// 先把MSE計算出來，再回傳PSNR值，
	se := 0.0
	for y := 0; y < imgH; y++ {
		for x := 0; x < imgW; x++ {
			se += math.Pow(float64(img2.GrayAt(x, y).Y)-float64(img1.GrayAt(x, y).Y), 2)
		}
	}
	mse := se / float64(imgW*imgH)
	return 10 * math.Log10(math.Pow(math.MaxUint8, 2)/mse)
}

// 當發生嚴重錯誤時紀錄錯誤訊息的函式。
func fatalWhenErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}
