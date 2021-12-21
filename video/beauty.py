# # -*- coding:utf-8 -*-
import cv2 as cv
import os
import numpy as np
import time


# 形态学处理
def Process(img):
    # 高斯平滑
    gaussian = cv.GaussianBlur(img, (3, 3), 0, 0, cv.BORDER_DEFAULT)
    # 中值滤波
    median = cv.medianBlur(gaussian, 5)
    # Sobel算子
    # 梯度方向: x
    sobel = cv.Sobel(median, cv.CV_8U, 1, 0, ksize=3)
    # 二值化
    ret, binary = cv.threshold(sobel, 170, 255, cv.THRESH_BINARY)
    # 核函数
    element1 = cv.getStructuringElement(cv.MORPH_RECT, (9, 1))
    element2 = cv.getStructuringElement(cv.MORPH_RECT, (9, 7))
    # 膨胀
    dilation = cv.dilate(binary, element2, iterations=1)
    # 腐蚀
    erosion = cv.erode(dilation, element1, iterations=1)
    # 膨胀
    dilation2 = cv.dilate(erosion, element2, iterations=3)
    return dilation2


def GetRegion(img):
    regions = []
    # 查找轮廓
    _, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv.contourArea(contour)
        if (area < 2000):
            continue
        eps = 1e-3 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, eps, True)
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        ratio =float(width) / float(height)
        if (ratio < 5 and ratio > 1.8):
            regions.append(box)
    return regions


def detect(img):
    # 灰度化
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    prc = Process(gray)

    regions = GetRegion(prc)
    print('[INFO]:Detect %d license plates' % len(regions))
    for box in regions:
        cv.drawContours(img, [box], 0, (0, 255, 0), 2)
    cv.imshow('Result', img)
    # cv.imwrite('result.jpg', img)
    cv.waitKey(2000)
    cv.destroyAllWindows()


def cap_detect():
    cap = cv.VideoCapture(0)

    if cap.isOpened() :
        print "video opened"

    lasttitle = ""
    while cap.isOpened():
        cv.waitKey(100)
        ret,img = cap.read()
        if ret == False:
            print "cap read false"
        else:
            #cv.imwrite('test.jpg',img)
            #image = cv.imread('test.jpg')
            cv.imshow("cap", img)
            try :
                detect(img)
            except:
                #continue
                #cv.destroyAllWindows()
                #lasttitle = "nuknown"
                #cv.imshow("nuknown", img)
                #cv.waitKey()
                print "except"
            else:
                print "else"

                #cv.waitKey(20)


    cap.release()
    cv.waitKey(0)
    cv.destroyAllWindow()


def cap_invent():
    cap = cv.VideoCapture(0)

    if cap.isOpened() :
        print "video opened"
        invent(cap)

    cap.release()
    cv.waitKey(0)
    cv.destroyAllWindow()

def invent(cap):
    lasttitle = ""
    frameCounter = 0
    previousFrame = None
    nextFrame = None
    iterations = 0
    backgroundImage = cv.imread("./bg.jpeg")
    # cv.imshow("bg",backgroundImage)
    while cap.isOpened():
        cv.waitKey(100)
        # cv.destroyAllWindows()
        ret,frame = cap.read()
        if ret == False:
            print "cap read false"
        else:
            # cv.imshow("cap", frame)
            cv.waitKey(100)
            try :
                if frameCounter % 2 == 1 :
                    nextFrame = frame
                if frameCounter % 2 == 0:
                    frameCounter = 0
                    previousFrame = frame
                frameCounter = frameCounter + 1
                iterations = iterations + 1
                if iterations > 2 :
                    print "invent",iterations
                    diff = cv.absdiff(previousFrame,nextFrame)
                    mask = cv.cvtColor(diff,cv.COLOR_BGR2GRAY)
                    th = 8
                    isMask = mask > th
                    nonMask = mask <= th
                    result = np.zeros_like(nextFrame,np.uint8)
                    resized = cv.resize(backgroundImage,(result,shape[1],result.shape[0]),interpolation = cv.INTER_AREA)
                    result[isMask] = nextFrame[isMask]
                    result[nonMask] = resized[nonMask]
                    print "invent"
                    cv.imshow("invent",result)
            except:
                print "except,%d",iterations
            else:
                print "else"

###################
#    main        #
# img = cv.imread('./test.jpg')
# detect(img)
#################

if __name__ == '__main__':
    img = cv.imread('./test.jpg')
    cap_invent()

