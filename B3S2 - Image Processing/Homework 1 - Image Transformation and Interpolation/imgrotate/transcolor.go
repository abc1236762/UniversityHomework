package imgrotate

import (
	`image/color`
	`math`
)

func transColorWithNNI(r *rotation, outX, outY int) *color.RGBA {
	inXF, inYF := r.antiTransXYWithOffset(outX, outY)
	inX, inY := int(math.RoundToEven(inXF)), int(math.RoundToEven(inYF))
	if (inX < 0 || inX >= r.inW) || (inY < 0 || inY >= r.inH) {
		return &color.RGBA{}
	}
	c := color.RGBAModel.Convert(r.inImg.At(inX, inY)).(color.RGBA)
	return &c
}

func transColorWithBI(r *rotation, outX, outY int) *color.RGBA {
	inXF, inYF := r.antiTransXYWithOffset(outX, outY)
	inX1, inX2 := int(math.Floor(inXF)), int(math.Ceil(inXF))
	inY1, inY2 := int(math.Floor(inYF)), int(math.Ceil(inYF))
	if (inX2 < 0 || inX1 >= r.inW) || (inY2 < 0 || inY1 >= r.inH) {
		return &color.RGBA{}
	}
	
	inXDeF, inYDeF := inXF-float64(inX1), inYF-float64(inY1)
	bI := func(sX1Y1, sX1Y2, sX2Y1, sX2Y2 uint8) uint8 {
		sX1Y1F, sX1Y2F := float64(sX1Y1), float64(sX1Y2)
		sX2Y1F, sX2Y2F := float64(sX2Y1), float64(sX2Y2)
		sY1F := sX1Y1F + inXDeF*(sX2Y1F-sX1Y1F)
		sY2F := sX1Y2F + inXDeF*(sX2Y2F-sX1Y2F)
		return uint8(math.RoundToEven(sY1F + inYDeF*(sY2F-sY1F)))
	}
	
	var cX1Y1, cX1Y2, cX2Y1, cX2Y2 color.RGBA
	if inX1 >= 0 && inY1 >= 0 {
		cX1Y1 = color.RGBAModel.Convert(r.inImg.At(inX1, inY1)).(color.RGBA)
	}
	if inX1 >= 0 && inY2 < r.inH {
		cX1Y2 = color.RGBAModel.Convert(r.inImg.At(inX1, inY2)).(color.RGBA)
	}
	if inX2 < r.inW && inY1 >= 0 {
		cX2Y1 = color.RGBAModel.Convert(r.inImg.At(inX2, inY1)).(color.RGBA)
	}
	if inX2 < r.inW && inY2 < r.inH {
		cX2Y2 = color.RGBAModel.Convert(r.inImg.At(inX2, inY2)).(color.RGBA)
	}
	
	return &color.RGBA{
		R: bI(cX1Y1.R, cX1Y2.R, cX2Y1.R, cX2Y2.R),
		G: bI(cX1Y1.G, cX1Y2.G, cX2Y1.G, cX2Y2.G),
		B: bI(cX1Y1.B, cX1Y2.B, cX2Y1.B, cX2Y2.B),
		A: bI(cX1Y1.A, cX1Y2.A, cX2Y1.A, cX2Y2.A),
	}
}
