import cv2 as cv
import numpy as np

# matrix with all 0's is empty black image, as 0 is for black
img = np.zeros((515, 512, 3), np.uint8)
# cv.imshow("Image", img)
# print(img.shape) # resulting (515, 512, 3)

# img[:] = 255, 0, 0
# cv.imshow("Image blue", img)

# img[img.shape[0]//4:3*(img.shape[0]//4), img.shape[1]//4:3*(img.shape[1]//4)] = 255, 0, 0
# cv.imshow("Image blue partial", img)

# cv.line(img, (img.shape[1]//4, img.shape[0]//4), (3*(img.shape[1]//4), 3*(img.shape[0]//4)), (0, 255, 255), 3)
# cv.imshow("Image with yellow line", img)

# cv.rectangle(img, (img.shape[1]//4, img.shape[0]//4), (3*(img.shape[1]//4), 3*(img.shape[0]//4)), (0, 255, 255), 2)
# cv.imshow("Image with yellow rectangle", img)

# cv.rectangle(img, (img.shape[1]//4, img.shape[0]//4), (3*(img.shape[1]//4), 3*(img.shape[0]//4)), (0, 255, 255), cv.FILLED)
# cv.imshow("Image with yellow rectangle filled", img)

# cv.circle(img, (img.shape[1]//2, img.shape[0]//2), img.shape[0]//4, (0, 255, 255), 5)
# cv.imshow("Image with yellow circle", img)
#
# cv.circle(img, (img.shape[1]//2, img.shape[0]//2), img.shape[0]//4, (0, 255, 255), cv.FILLED)
# cv.imshow("Image with yellow circle filled", img)

cv.putText(img, "CChCheChen", (img.shape[1]//3, img.shape[0]//2), cv.FONT_HERSHEY_COMPLEX, 0.8, (0, 150, 0), 2)
cv.imshow("Image with text", img)

cv.waitKey(0)