import cv2 as cv
import numpy as np

units = 120
img_e = units * 4

floor = cv.imread('tile_texture7.jpg')
floor = cv.resize(floor, (units * 2, units * 2), interpolation=cv.INTER_CUBIC)
wall = cv.imread('tile_texture9.jpg')
wall_oh, wall_ow, _ = wall.shape
wall_projective_mat = cv.getPerspectiveTransform(
    np.float32([[0, 0], [wall_ow-1, 0],
                [0, wall_oh-1], [wall_ow-1, wall_oh-1]]),
    np.float32([[0, 0], [units*4-1, 0],
                [units-1, units-1], [units*3-1, units-1]]))
wall = cv.warpPerspective(wall, wall_projective_mat, (img_e, img_e))

img = np.zeros((img_e, img_e, 3), np.uint8)
img[units:units*3, units:units*3, :] = floor
for angle in range(0, 360, 90):
    rotation_mat = cv.getRotationMatrix2D((img_e // 2, img_e // 2), angle, 1)
    img = cv.add(img, cv.warpAffine(wall, rotation_mat, (img_e, img_e)))

cv.imshow('img', img)
cv.waitKey()
cv.destroyAllWindows()
