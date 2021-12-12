import cv2 as cv
import numpy as np

img = cv.imread("Resources/cards.png")
cv.imshow("Cards", img)

width, height = 250, 350

pts1 = np.float32([[354, 177], [450, 200], [314, 286], [420, 315]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

matrix = cv.getPerspectiveTransform(pts1, pts2)

imgOutput = cv.warpPerspective(img, matrix, (width, height))
cv.imshow("Cards output", imgOutput)

cv.waitKey(0)