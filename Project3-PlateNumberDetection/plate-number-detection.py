import cv2 as cv
import numpy as np

# ---------- Read Web-cams ----------
frameWidth = 640
frameHeight = 480
PlateNumberCascade = cv.CascadeClassifier("../Resources/haarcascade_russian_plate_number.xml")
minArea = 200
color = (255, 0, 255)

capture = cv.VideoCapture(0)
capture.set(3, frameWidth)
capture.set(4, frameHeight)
capture.set(10, 150)
count = 0

while True:
    success, img = capture.read()
    if success:
        imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        numberPlates = PlateNumberCascade.detectMultiScale(imgGray, 1.1, 10)
        for (x, y, w, h) in numberPlates:
            area = w * h
            if area > minArea:
                cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv.putText(img, "Plate Number", (x, y - 5), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
                imgRoi = img[y:y + h, x:x + w]
                cv.imshow("ROI", imgRoi)

        cv.imshow("Result", img)

        if cv.waitKey(1) & 0xFF == ord('s'):
            print("Before", count)
            cv.imwrite("ScannerPlateNumber/NoPlate_" + str(count) + ".jpg", imgRoi)
            cv.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv.FILLED)
            cv.putText(img, "Scan Saved", (150, 265), cv.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
            cv.imshow("Result", img)
            cv.waitKey(500)
            print("After", count)
            count += 1
    else:
        break

capture.release()
cv.destroyAllWindows()