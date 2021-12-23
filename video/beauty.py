# # -*- coding:utf-8 -*-
import cv2 as cv
import os
import numpy as np
import time
import sys


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


def cap_invent(th):
    cap = cv.VideoCapture(0)

    if cap.isOpened() :
        print "video opened"
        invent(cap,th)

    cap.release()
    cv.waitKey(0)
    cv.destroyAllWindow()

def invent(cap,th):
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
                    cv.imshow("diff", diff)
                    # cv.waitKey(100)
                    mask = cv.cvtColor(diff,cv.COLOR_BGR2GRAY)
                    cv.imshow("mask", mask)
                    # cv.waitKey(100)
                    # th = 3
                    isMask = mask > th
                    nonMask = mask <= th
                    result = np.zeros_like(nextFrame,np.uint8)
                    resized = cv.resize(backgroundImage,(result.shape[1],result.shape[0]),interpolation = cv.INTER_AREA)
                    # cv.imshow("cap", resized)
                    # cv.waitKey(100)
                    result[isMask] = nextFrame[isMask]
                    result[nonMask] = resized[nonMask]
                    print "invent"
                    cv.imshow("invent",result)
            except Exception as ex :
                print "except,%s"%ex,iterations
            else:
                print "else"


# TODO 背景减除算法集合
ALGORITHMS_TO_EVALUATE = [
    (cv.bgsegm.createBackgroundSubtractorGMG(20, 0.7), 'GMG'),
    (cv.createBackgroundSubtractorKNN(), 'KNN'),
    (cv.bgsegm.createBackgroundSubtractorMOG(), 'MOG'),
    (cv.createBackgroundSubtractorMOG2(), 'MOG2'),
]


def bg(num):
    # 背景分割识别器序号
    algo_index = num
    subtractor = ALGORITHMS_TO_EVALUATE[algo_index][0]
    show_fgmask = False

    # 获得运行环境CPU的核心数
    nthreads = cv.getNumberOfCPUs()
    # 设置线程数
    cv.setNumThreads(nthreads)

    # 读取视频
    # capture = cv.VideoCapture(videoPath)
    capture = cv.VideoCapture(0)

    # 当前帧数
    frame_num = 0

    while True:
        ret, frame = capture.read()
        if not ret:
            print "not cap"
            return
        fgmask = subtractor.apply(frame)

        cv.imshow("fgmask",fgmask)
        cv.waitKey(200)


        mask = np.zeros(frame.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (1,1,frame.shape[1]-2,frame.shape[0]-2)
        iteration = 5

        if show_fgmask:
            segm = fgmask
        else:
            segm = (frame * 0.5).astype('uint8')
            cv.add(frame, (100, 0, 0, 0), segm, fgmask)
        cv.imshow('some', segm)
        cv.waitKey(200)



        cv.grabCut(frame, mask, rect, bgdModel, fgdModel,
                    iteration, cv.GC_INIT_WITH_RECT)
        cv.imshow("grabCut",frame)
        cv.waitKey(200)

        key = cv.waitKey(1) & 0xFF
        frame_num = frame_num + 1

        # 按'q'健退出循环
        if key == ord('q'):
            break

    cv.destroyAllWindows()


###################
#    main        #
# img = cv.imread('./test.jpg')
# detect(img)
#################

if __name__ == '__main__':
    arg = 0
    if len(sys.argv) > 1:
        arg = int(sys.argv[1])
    # img = cv.imread('./test.jpg')
    # cap_invent(arg)
    bg(arg)

