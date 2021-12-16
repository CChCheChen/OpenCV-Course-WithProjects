import cv2 as cv
import numpy as np

# ---------- Read Web-cams ----------
frameWidth = 480
frameHeight = 640
capture = cv.VideoCapture(0)
capture.set(3, frameWidth)
capture.set(4, frameHeight)
capture.set(10, 150)

# ---------- Pre-process image ----------
def preProcessing(img):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv.Canny(imgBlur, 200, 200)
    # return imgCanny

    kernel = np.ones((5, 5))
    imgDial = cv.dilate(imgCanny, kernel, iterations=2)
    imgErode = cv.erode(imgDial, kernel, iterations=1)
    return imgErode

# ---------- Find the largest contour available ----------
def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)

        if area > 5000:
            # cv.drawContours(imageContours, cnt, -1, (255, 0, 0), 2)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area

            # print(len(approx)) # it should be 4 for page document
    cv.drawContours(imgContours, biggest, -1, (255, 0, 0), 20)
    return biggest

# ---------- Re-order for word warp ----------
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    # print("add",  add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]

    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("New Points", myPointsNew)
    return myPointsNew


# ---------- Send for word warp perspective ----------
def getWarp(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [frameWidth, 0], [0, frameHeight], [frameWidth, frameHeight]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv.warpPerspective(img, matrix, (frameWidth, frameHeight))
    imgCropped = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]
    imgCropped = cv.resize(imgCropped, (frameWidth, frameHeight))
    return imgCropped

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
                if len(imgArray[x][y].shape) == 2:imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
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
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

while True:
    success, img = capture.read()

    # Resize image
    img = cv.resize(img, (frameWidth, frameHeight))

    imgContours = img.copy()
    imgThreshold = preProcessing(img)

    biggest = getContours(imgThreshold)
    print(biggest)
    if biggest.size != 0:
        imgWarped = getWarp(img, biggest)
        imageArray = ([img, imgThreshold],
                      [imgContours, imgWarped])
        # imageArray = ([imageContours, imgWarped])
        cv.imshow("ImageWarped", imgWarped)
    else:
        imageArray = ([img, imgContours])

    stackedImages = stackImages(0.6, imageArray)

    if success:
        cv.imshow("Result", stackedImages)
        if cv.waitKey(1) & 0xFF == ord('d'):
            break
    else:
        break

capture.release()
cv.destroyAllWindows()