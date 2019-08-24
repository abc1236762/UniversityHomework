package main

import (
	"flag"
	"image"
	`image/gif`
	"image/jpeg"
	`image/png`
	"log"
	`math`
	"os"
	`path/filepath`
	`strings`
	
	`golang.org/x/image/bmp`
	`golang.org/x/image/tiff`
	_ `golang.org/x/image/webp`
	
	`./imgrotate`
)

var (
	inImgPath  = flag.String("i", "", `input image file's path`)
	outImgPath = flag.String("o", "", `output image file's path (optional)`)
	outImgFmt  = flag.String("f", "", `output image file's format [
	"bmp" | "gif" | "jpeg" | "png" | "tiff"
] (optional)`)
	angle  = flag.Float64("a", 0.0, `rotation angle in degrees`)
	method = flag.String("m", "NNI", `method of image rotation [
	"NNI" (Nearest-Neighbor Interpolation) |
	"BI" (Bilinear Interpolation)
]`)
)

func init() {
	log.SetOutput(os.Stdout)
	
	flag.Parse()
	if *inImgPath == "" {
		log.Fatalln("required flag -i and its value")
	}
	*outImgFmt = strings.ToLower(*outImgFmt)
	*method = strings.ToUpper(*method)
}

func main() {
	inImg := openImg(*inImgPath)
	var rotateMethod imgrotate.RotateMethod
	switch *method {
	case "NNI":
		rotateMethod = imgrotate.NNI
	case "BI":
		rotateMethod = imgrotate.BI
	}
	outImg := imgrotate.Rotate(inImg, (*angle)/180*math.Pi, rotateMethod)
	saveImg(*outImgPath, outImg)
}

func openImg(imgPath string) image.Image {
	imgFile, err := os.Open(imgPath)
	fatalWhenErr(err)
	defer func() {
		fatalWhenErr(imgFile.Close())
	}()
	
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

func saveImg(imgPath string, img image.Image) {
	imgFile, err := os.Create(imgPath)
	fatalWhenErr(err)
	defer func() {
		fatalWhenErr(imgFile.Close())
	}()
	
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

func fatalWhenErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}
