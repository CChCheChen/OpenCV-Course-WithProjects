import cv2 as cv
import numpy as np

kernel = np.ones((5, 5), np.uint8)

img = cv.imread("Resources/fred.png")
# cv.imshow("Fred", img)

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow("Fred Gray", img_gray)

img_blur = cv.GaussianBlur(img_gray, (7, 7), 0)
# cv.imshow("Fred Blur", img_blur)

img_canny1 = cv.Canny(img, 100, 100)
# cv.imshow("Fred Canny 1", img_canny1)
img_canny2 = cv.Canny(img, 150, 200)
# cv.imshow("Fred Canny 2", img_canny2)

img_dilation1 = cv.dilate(img_canny1, kernel, iterations=1)
# cv.imshow("Fred Dilation 1", img_dilation1)
img_dilation2 = cv.dilate(img_canny1, kernel, iterations=5)
# cv.imshow("Fred Dilation 2", img_dilation2)

img_eroded1 = cv.erode(img_dilation1, kernel, iterations=1)
cv.imshow("Fred Eroded 1", img_eroded1)
img_eroded2 = cv.erode(img_dilation1, kernel, iterations=0)
cv.imshow("Fred Eroded 2", img_eroded2)

cv.waitKey(0)