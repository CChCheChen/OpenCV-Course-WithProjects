import cv2 as cv
import numpy as np

# ---------- Read Web-cams ----------
frameWidth = 640
frameHeight = 480
capture = cv.VideoCapture(0)
capture.set(3, frameWidth)
capture.set(4, frameHeight)
capture.set(10, 150)

myColors = [[5, 107, 0, 19, 255, 255],
            [133, 56, 0, 159, 156, 255],
            [57, 76, 0, 100, 255, 255],
            [90, 48, 0, 118, 255, 255]]
myColorValues = [[255, 255, 0],
                 [51, 153, 255],
                 [0, 204, 102],
                 [255, 0, 0]]
myPoints = []  ## [x , y , colorId ]

def findColor(img, myColors, myColorValues):
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv.circle(frame_result, (x, y), 15, myColorValues[count], cv.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv.imshow(str(color[0]), mask)
    return newPoints

def getContours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500:
            # cv.drawContours(frame_result, cnt, -1, (255, 0, 0), 3)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv.boundingRect(approx)
    return x + w//2, y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv.circle(frame_result, (point[0], point[1]), 10, myColorValues[point[2]], cv.FILLED)

while True:
    success, frame = capture.read()
    frame_result = frame.copy()

    new_points = findColor(frame, myColors, myColorValues)
    if len(new_points) != 0:
        for newP in new_points:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    if success:
        cv.imshow('Result', frame_result)
        if cv.waitKey(1) & 0xFF == ord('d'):
            break
    else:
        break

capture.release()
cv.destroyAllWindows()