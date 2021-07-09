import os
from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
# def classify_gray_hist(image1,image2,size=(256,256)):
#     image1 = cv2.resize(image1, size)
#     image2 = cv2.resize(image2, size)
#     hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
#     hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
#     # 可以比较下直方图
#     #plt.plot(range(256), hist1, 'r')
#     #plt.plot(range(256), hist2, 'b')
#     #plt.show()
#     # 计算直方图的重合度
#     degree = 0
#     for i in range(len(hist1)):
#         if hist1[i] != hist2[i]:
#             degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
#     else:
#         degree = degree + 1
#     degree = degree / len(hist1)
#     return degree


# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
    else:
        degree = degree + 1
    degree = degree / len(hist1)
    return degree


# 通过得到每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data

#
# # 平均哈希算法计算
# def classify_aHash(image1, image2):
#     image1 = cv2.resize(image1, (8, 8))
#     image2 = cv2.resize(image2, (8, 8))
#     gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
#     gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
#     hash1 = getHash(gray1)
#     hash2 = getHash(gray2)
#     return Hamming_distance(hash1, hash2)

#
# def classify_pHash(image1, image2):
#     image1 = cv2.resize(image1, (32, 32))
#     image2 = cv2.resize(image2, (32, 32))
#     gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
#     gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
#     # 将灰度图转为浮点型，再进行dct变换
#     dct1 = cv2.dct(np.float32(gray1))
#     dct2 = cv2.dct(np.float32(gray2))
#     # 取左上角的8*8，这些代表图片的最低频率
#     # 这个操作等价于c++中利用opencv实现的掩码操作
#     # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
#     dct1_roi = dct1[0:8, 0:8]
#     dct2_roi = dct2[0:8, 0:8]
#     hash1 = getHash(dct1_roi)
#     hash2 = getHash(dct2_roi)
#     return Hamming_distance(hash1, hash2)


# 输入灰度图，返回hash
# def getHash(image):
#     avreage = np.mean(image)
#     hash = []
#     for i in range(image.shape[0]):
#         for j in range(image.shape[1]):
#             if image[i, j] > avreage:
#                 hash.append(1)
#             else:
#                 hash.append(0)
#     return hash
#
#
# # 计算汉明距离
# def Hamming_distance(hash1, hash2):
#     num = 0
#     for index in range(len(hash1)):
#         if hash1[index] != hash2[index]:
#             num += 1
#     return num


if __name__ == '__main__':
    # 读取所有图片路径
    pathall = []
    img1 = cv2.imread('/Users/lucong/Desktop/test.jpg')
    minn=10000.0
    minn_path=""
    i = 0
    for path in os.listdir("/Volumes/硬盘/clothes_image_all_final/training"):
        if path.startswith():
            img2 = cv2.imread('/Volumes/硬盘/clothes_image_all_final/training/'+path)
            degree1 = classify_hist_with_split(img1, img2)
            if minn > degree1:
                minn = degree1
                minn_path = '/Volumes/硬盘/clothes_image/training_old/'+path
                img3 = img2
            if i%1000==0 :
                print(i,minn_path)
            i += 1

    # cv2.imshow('img1', img1)
    cv2.imshow('img3', img3)
    # img3 = cv2.imread('/Volumes/硬盘/clothes_image/training/0_131.jpg')
    # img4 = cv2.imread('/Volumes/硬盘/clothes_image/training/0_131.jpg')
    #cv2.imshow('img3',img3)
    # degree2 = classify_gray_hist(img1,img3)
    # degree3 = classify_gray_hist(img2, img3)
    # degree4 = classify_gray_hist(img4, img3)
    # degree = classify_hist_with_split(img1,img2)
    # degree = classify_aHash(img1,img2)
    # degree = classify_pHash(img1,img2)
    # print(degree1)
    # if degree3 <degree4:
    #     cv2.imshow('img2',img2)
    # else:
    #     cv2.imshow('img4',img4)
    # # if degree1<degree2:
    # #     cv2.imshow('img2', img2)
    # # else:
    # #     cv2.imshow('img3', img3)
    cv2.waitKey(0)