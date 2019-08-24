package imgrotate

import (
	"image"
	`image/color`
	`log`
	`math`
)

type RotateMethod int

const (
	NNI RotateMethod = iota
	BI
)

type rotation struct {
	inImg                image.Image
	outImg               *image.RGBA
	inW, inH, outW, outH int
	offsetX, offsetY     float64
	angle                float64
	transColorFunc       func(r *rotation, outX, outY int) *color.RGBA
}

func Rotate(inImg image.Image, angle float64, method RotateMethod) image.Image {
	r := newRotation(inImg, angle)
	switch method {
	case NNI:
		r.transColorFunc = transColorWithNNI
	case BI:
		r.transColorFunc = transColorWithBI
	default:
		log.Fatalf("rotate method (value \"%v\") is not supported\n", method)
	}
	r.rotate(method)
	return r.outImg
}

func newRotation(inImg image.Image, angle float64) (r *rotation) {
	r = &rotation{inImg: inImg, angle: angle}
	r.makeOutImg()
	return r
}

func (r *rotation) makeOutImg() {
	inRect := r.inImg.Bounds()
	r.inW, r.inH = inRect.Max.X, inRect.Max.Y
	transXF, transYF := make([]float64, 4, 4), make([]float64, 4, 4)
	transXF[0], transYF[0] = r.transXY(0, 0)
	transXF[1], transYF[1] = r.transXY(0, r.inH)
	transXF[2], transYF[2] = r.transXY(r.inW, 0)
	transXF[3], transYF[3] = r.transXY(r.inW, r.inH)
	
	getFloat64MinMax := func(arr []float64) (min, max float64) {
		min, max = arr[0], arr[0]
		for _, val := range arr {
			if val > max {
				max = val
			}
			if val < min {
				min = val
			}
		}
		return
	}
	
	outMinXF, outMaxXF := getFloat64MinMax(transXF)
	outMinYF, outMaxYF := getFloat64MinMax(transYF)
	r.outW = int(math.RoundToEven(outMaxXF - outMinXF))
	r.outH = int(math.RoundToEven(outMaxYF - outMinYF))
	r.offsetX = (outMinXF + outMaxXF - float64(r.outW)) / 2
	r.offsetY = (outMinYF + outMaxYF - float64(r.outH)) / 2
	r.outImg = image.NewRGBA(image.Rectangle{
		Min: image.Point{}, Max: image.Point{X: r.outW, Y: r.outH},
	})
}

func (r *rotation) rotate(method RotateMethod) image.Image {
	for outY := 0; outY < r.outH; outY++ {
		for outX := 0; outX < r.outW; outX++ {
			c := r.transColorFunc(r, outX, outY)
			r.outImg.SetRGBA(outX, outY, *c)
		}
	}
	return r.outImg
}

func (r *rotation) transXY(x, y int) (float64, float64) {
	xF, yF := float64(x), float64(y)
	return xF*math.Cos(r.angle) + yF*-math.Sin(r.angle),
		xF*math.Sin(r.angle) + yF*math.Cos(r.angle)
}

func (r *rotation) antiTransXYWithOffset(x, y int) (float64, float64) {
	xF, yF := float64(x)+r.offsetX, float64(y)+r.offsetY
	return xF*math.Cos(r.angle) + yF*math.Sin(r.angle),
		xF*-math.Sin(r.angle) + yF*math.Cos(r.angle)
}
