import cv2 as cv

print("Package Imported")

# ---------- Read images ----------
# img = cv.imread("Resources/monday.jpg")
# cv.imshow("Monday", img)

# img = cv.imread("Resources/fred.png")
# cv.imshow("Fred", img)
#
# cv.waitKey(0)

# ---------- Read videos ----------
# capture = cv.VideoCapture("Resources/monday.MP4")
# while True:
#     success, frame = capture.read()
#
#     if success:
#         cv.imshow('Monday', frame)
#         if cv.waitKey(20) & 0xFF == ord('d'):  # close window when 'd' is pressed on keyboard
#             break
#     else:
#         break
#
# capture.release()
# cv.destroyAllWindows()

# ---------- Read Web-cams ----------
capture = cv.VideoCapture(0) # for default web-cam
capture.set(3, 630)
capture.set(4, 480)

while True:
    success, frame = capture.read()

    if success:
        cv.imshow('Monday', frame)
        if cv.waitKey(20) & 0xFF == ord('d'):  # close window when 'd' is pressed on keyboard
            break
    else:
        break

capture.release()
# cv.destroyAllWindows()