import cv2 as cv

cap = cv.VideoCapture(0)
fps = 10
fourcc = cv.VideoWriter_fourcc(*'mp4v')
sz = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
vout = cv.VideoWriter()
vout.open('./sample.mp4',fourcc,fps,sz)
cnt = 0
while cnt < 20 :
    ret,frame = cap.read()
    vout.write(frame)
    cnt += 1
vout.release()
cap.release()

