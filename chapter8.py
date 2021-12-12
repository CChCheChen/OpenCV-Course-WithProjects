import cv2 as cv
import numpy as np

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        # print(area)

        # Draw the contour
        if area > 500:
            cv.drawContours(img_contour, cnt, -1, (255, 0, 0), 2)

            # Calculate the curve length
            peri = cv.arcLength(cnt, True)
            # print(peri)

            # Approximate the corner points
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            print(len(approx))

            # Create object corners
            obj_corner = len(approx)

            # Create bonding box around the detected object corners
            x, y, w, h = cv.boundingRect(approx)

            if obj_corner == 3: obj_type = "Triangle"
            elif obj_corner == 4:
                aspRatio = w / float(h)
                if aspRatio > 0.98 and aspRatio < 1.02: obj_type = "Square"
                else:
                    obj_type = "Rectangle"
            elif obj_corner > 4:
                obj_type = "Circles"
            else:
                obj_type = "None"

            cv.rectangle(img_contour, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv.putText(img_contour, obj_type, (x + (w // 2) - 10, y + (h // 2) - 10), cv.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 1)


img = cv.imread('Resources/shapes.png')

img_contour = img.copy()

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_blur = cv.GaussianBlur(img_gray, (7, 7), 1)
img_canny = cv.Canny(img_blur, 50, 50)

getContours(img_canny)

img_black = np.zeros_like(img)
img_stacked = stackImages(0.9, ([img, img_gray, img_blur], [img_canny, img_contour, img_black]))

cv.imshow("ImageStack", img_stacked)
cv.waitKey(0)