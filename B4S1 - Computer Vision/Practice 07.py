import cv2 as cv
import numpy as np

kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))

img = cv.imread('red_blood_cell.jpg', cv.IMREAD_GRAYSCALE)
img = cv.erode(img, kernel, iterations=1)
img = cv.dilate(img, kernel, iterations=1)
edges = cv.Canny(img, 160, 240)
circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, 12, param1=20,
                          param2=12, minRadius=6, maxRadius=11)[0]
circles = np.uint32(np.around(circles))

circles_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
for i in circles:
    cv.circle(circles_img, (i[0], i[1]), i[2], (0x00, 0xFF, 0x00), 1)
cv.putText(circles_img, str(len(circles)), (0, 36),
           cv.FONT_HERSHEY_SIMPLEX, 1.5, (0xFF, 0x00, 0xFF), 2, cv.LINE_AA)

cv.imshow('circles', circles_img)
cv.waitKey(0)
cv.destroyAllWindows()
