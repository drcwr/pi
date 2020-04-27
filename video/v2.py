import cv2 as cv

cv.namedWindow("Image")

cap = cv.VideoCapture(0)

if cap.isOpened() :
    print "video opened"

while cap.isOpened():
    ret,img = cap.read()
    if ret == False:
        print "cap read false"
    else:
        cv.imshow('Image',img)
        k = cv.waitKey(100)
        if k == ord('a') or k == ord('A'):
            cv.imwrite('test.jpg',img)
            break

cap.release()
cv.waitKey(0)
cv.destroyAllWindow()
