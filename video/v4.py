# # -*- coding:utf-8 -*-
import cv2 as cv
import os
import numpy as np
import time

# 检测人脸


def detect_face(img):
    #将测试图像转换为灰度图像，因为opencv人脸检测器需要灰度图像
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #加载OpenCV人脸检测分类器Haar
    face_cascade = cv.CascadeClassifier('./haarcascade_frontalface_default.xml')
    #检测多尺度图像，返回值是一张脸部区域信息的列表（x,y,宽,高）
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    # 如果未检测到面部，则返回原始图像
    if (len(faces) == 0):
        return None, None
    #目前假设只有一张脸，xy为左上角坐标，wh为矩形的宽高
    (x, y, w, h) = faces[0]
    #返回图像的正面部分
    return gray[y:y + w, x:x + h], faces[0]

# 该函数将读取所有的训练图像，从每个图像检测人脸并将返回两个相同大小的列表，分别为脸部信息和标签
def prepare_training_data(data_folder_path):
    # 获取数据文件夹中的目录（每个主题的一个目录）
    dirs = os.listdir(data_folder_path)
    # 两个列表分别保存所有的脸部和标签
    faces = []
    labels = []
    names = {}
    # 浏览每个目录并访问其中的图像
    print "dirs ",dirs
    for dir_name in dirs:
        # dir_name(str类型)即标签
        label = int(dir_name)
        print "train label ",label
        # 建立包含当前主题主题图像的目录路径
        subject_dir_path = data_folder_path + "/" + dir_name
        # 获取给定主题目录内的图像名称
        subject_images_names = os.listdir(subject_dir_path)
        # 浏览每张图片并检测脸部，然后将脸部信息添加到脸部列表faces[]
        for image_name in subject_images_names:
            shotname, extension = os.path.splitext(image_name)
            print "filename,ext",shotname,extension
            if extension == ".name":
                names[dir_name]= shotname
            else:
                # 建立图像路径
                image_path = subject_dir_path + "/" + image_name
                # 读取图像
                image = cv.imread(image_path)

                # 检测脸部
                face, rect = detect_face(image)
                # 我们忽略未检测到的脸部
                if face is not None:
                #将脸添加到脸部列表并添加相应的标签
                    faces.append(face)
                    labels.append(label)
                    cv.waitKey(1)
                    cv.destroyAllWindows()
    #最终返回值为人脸和标签列表
    print "labels,names",labels,names
    return faces, labels,names


#根据给定的（x，y）坐标和宽度高度在图像上绘制矩形
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv.rectangle(img, (x, y), (x + w, y + h), (128, 128, 0), 2)

# 根据给定的（x，y）坐标标识出人名
def draw_text(img, text, x, y):
    cv.putText(img, text, (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (128, 128, 0), 2)

# 此函数识别传递的图像中的人物并在检测到的脸部周围绘制一个矩形及其名称
def predict(test_img):
    #生成图像的副本，这样就能保留原始图像
    img = test_img.copy()
    #检测人脸
    face, rect = detect_face(img)
    #预测人脸
    label = face_recognizer.predict(face)
    print "label",label
    # 获取由人脸识别器返回的相应标签的名称
    #label_text = subjects[label[0]]
    if label[0] >= len(names):
        label_text = "nuknown-" + str(label[1])
    else:
        label_text = names[str(label[0])] + "-" + str(label[1])
    # 在检测到的脸部周围画一个矩形
    draw_rectangle(img, rect)
    # 标出预测的名字
    draw_text(img, label_text, rect[0], rect[1] - 5)
    #返回预测的图像
    return img,label[0]


#调用prepare_training_data（）函数
faces, labels, names = prepare_training_data("training_data")

#创建LBPH识别器并开始训练，当然也可以选择Eigen或者Fisher识别器
face_recognizer = cv.face.createLBPHFaceRecognizer()
face_recognizer.train(faces, np.array(labels))

pre_dir_path = "test_data"
pre_images_names = os.listdir(pre_dir_path)
    # 浏览每张图片并检测脸部，然后将脸部信息添加到脸部列表faces[]
for image_name in pre_images_names:
    shotname, extension = os.path.splitext(image_name)
    image_path = pre_dir_path + "/" + image_name
    # 读取图像
    image = cv.imread(image_path)
    predicted_img,subid = predict(image)
    if subid >= len(names):
        cv.imshow("nuknown", predicted_img)
    else:
        print "names subid",names[str(subid)]
        cv.imshow(names[str(subid)], predicted_img)            

    cv.waitKey(1000)
    cv.destroyAllWindows()



###################
#
#    main        #
#
#################

cap = cv.VideoCapture(0)

if cap.isOpened() :
    print "video opened"

lasttitle = ""
while cap.isOpened():
    ret,img = cap.read()
    if ret == False:
        print "cap read false"
    else:
        #cv.imwrite('test.jpg',img)
        #image = cv.imread('test.jpg')
        cv.imshow("cap", img)

        # save cap image
        k = cv.waitKey(30)
        print("wait end",ord('a'),k)
        if k == ord('a') or k == ord('A'):
            cv.imwrite('test-'+str(time.time())+'.jpg',img)

        try :
            predicted_img,subid = predict(img)
        except:
            #continue
            #cv.destroyAllWindows()
            #lasttitle = "nuknown"
            #cv.imshow("nuknown", img)
            #cv.waitKey()
            print ""
        else:
            title = ""
            if subid >= len(names):
                title = "nuknown"
            else:
                print "names subid",names[str(subid)]
                title = names[str(subid)]
                
            if lasttitle != title:
                lasttitle = title
                #cv.destroyAllWindows()
                cv.imshow(title, predicted_img)            

            #cv.waitKey(20)


cap.release()
cv.waitKey(0)
cv.destroyAllWindow()
