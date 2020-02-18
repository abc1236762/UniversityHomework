import cv2 as cv
import numpy as np

img = cv.imread('gear_tooth.png', cv.IMREAD_GRAYSCALE)[26:147, 48:252]

img_a = cv.threshold(img, 0xE1, 0xFF, cv.THRESH_BINARY)[1]
cv.imshow('(a)', img_a)

kernel_dot = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
kernel_hole = cv.getStructuringElement(cv.MORPH_ELLIPSE, (30, 30))
kernel_hole_e = cv.erode(kernel_hole, kernel_dot, iterations=1)
kernel_hole_ring = kernel_hole - kernel_hole_e

img_b = cv.erode(img_a, kernel_hole_ring, iterations=1)
cv.imshow('(b)', img_b)

img_c = cv.dilate(img_b, kernel_hole, iterations=1)
cv.imshow('(c)', img_c)

img_d = cv.bitwise_or(img, img_c)
cv.imshow('(d)', img_d)

gear_body = cv.getStructuringElement(cv.MORPH_ELLIPSE, (57, 57))
sampling_ring_spacer = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 2))
sampling_ring_width = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

img_e1 = cv.morphologyEx(img_d, cv.MORPH_OPEN, gear_body)
img_e2 = cv.dilate(img_e1, sampling_ring_spacer, iterations=1)
img_e3 = cv.dilate(img_e2, sampling_ring_width, iterations=1)
img_e = cv.subtract(img_e3, img_e2)
cv.imshow('(e)', img_e)

img_f = cv.bitwise_and(img, img_e)
cv.imshow('(f)', img_f)

tip_spacing = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

img_g = cv.dilate(img_f, tip_spacing, iterations=1)
img_g = cv.convertScaleAbs(img_g, alpha=3)
cv.imshow('(g)', img_g)

defect_cue = cv.getStructuringElement(cv.MORPH_ELLIPSE, (13, 13))

img_h = cv.subtract(img_e, img_g)
img_h = cv.dilate(img_h, defect_cue, iterations=1)
img_h = cv.bitwise_or(img_h, img_g)
img_h = cv.convertScaleAbs(img_h, alpha=3)
cv.imshow('(h)', img_h)

cv.waitKey()
cv.destroyAllWindows()
