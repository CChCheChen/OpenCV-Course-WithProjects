import cv2 as cv
import numpy as np

faceCascade = cv.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

img = cv.imread("Resources/lakers.jpg")
# cv.imshow("Lakers", img)

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(img_gray, 1.02, 9)

for (x, y, w, h) in faces:
    cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

cv.imshow("Lakers face detected", img)

cv.waitKey(0)