import os
import random
import shutil
#读取所有图片路径
pathall = []
for path in os.listdir("/Volumes/硬盘/clothes_image_all"):
    pathall.append(path)
#打乱数据
random.shuffle(pathall)
#将数据分为训练集、验证集
length = len(pathall)
train_set_path = pathall[:int(0.7*length)]
test_set_path = pathall[int(0.7*length):]
print(len(train_set_path))
print(len(test_set_path))
tmp1 = [[] for x in range(23)]
tmp2 = [[] for x in range(23)]
for trainpath in train_set_path:
    for i in range(23):
        str1 = str(i)+"_"
        if trainpath.startswith(str1):
            sourcepath1 = os.path.join("/Volumes/硬盘/clothes_image_all/",trainpath)     #原路径
            newpath1 = "/Volumes/硬盘/clothes_image/training"+"/"+str(i)+"_"+str(len(tmp1[i]))+".jpg"   #新路径，放到training文件夹中，并按类别_顺序命名"
            shutil.copyfile(sourcepath1,newpath1)
            tmp1[i].append(1)
for testpath in test_set_path:
    for j in range(23):
        str2 = str(j)+"_"
        if testpath.startswith(str2):
            sourcepath2 = os.path.join("/Volumes/硬盘/clothes_image_all/",testpath)
            newpath2 = "/Volumes/硬盘/clothes_image/test"+"/"+str(j)+"_"+str(len(tmp2[j]))+".jpg"
            shutil.copyfile(sourcepath2,newpath2)
            tmp2[j].append(1)
