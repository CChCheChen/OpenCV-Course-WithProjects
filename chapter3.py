import cv2 as cv

img = cv.imread("Resources/fred.png")
cv.imshow("Fred", img)
# print(img.shape) # resulting (480, 852, 3) where 480 is height and  852 is width, 3 is color channel for BGR

img_resize = cv.resize(img, (img.shape[1]*2, img.shape[0]*2)) # (width, height)
# cv.imshow("Fred resized", img_resize)
# print(img_resize.shape) # resulting (960, 1704, 3)

img_cropped = img[img.shape[0]//4:3*(img.shape[0]//4), img.shape[1]//4:3*(img.shape[1]//4)] # (height, width)
cv.imshow("Fred cropped", img_cropped)

cv.waitKey(0)