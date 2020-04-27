import cv2 as cv
import time
cv.namedWindow("Image")

cap = cv.VideoCapture(0)

if cap.isOpened() :
    print "video opened"

while cap.isOpened():
    ret,img = cap.read()
    if ret == False:
        print "cap read false"
    else:
        #cv.imshow('Image',img)
        faceCascade = cv.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
        faces = faceCascade.detectMultiScale(img,scaleFactor = 1.1,minNeighbors = 5,minSize = (10,10),flags = cv.CASCADE_SCALE_IMAGE)
        #cv.putText(img,"Find"+str(len(faces))+"faces",(10,img.shape[0]-5),cv.FONT_HERSHEY_SIMPLEX,1,(255,232,133),2)
        #for (x,y,w,h) in faces:
        #   cv.rectangle(img,(x,y),(x+w,y+h),(128,255,0),2)
            #print(x,y,w,h)
            #cv.imshow('Image',img)
        cv.imshow('Image',img)
        k = cv.waitKey(30)
        #print("wait end")
        if k == ord('a') or k == ord('A'):
            cv.imwrite('test-'+str(time.time())+'.jpg',img)

cap.release()
cv.waitKey(0)
cv.destroyAllWindow()
