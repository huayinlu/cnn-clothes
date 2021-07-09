import os
import json
from PIL import Image

def explain_json(path,pictures_path):
    with open(path, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        img_name = ret_dic['img_name']
        num = img_name[0] #取出itemID“000123”
        # 获取图片路径'/Volumes/硬盘/train_dataset_part1/image/000123/0.jpg’
        picture_path = pictures_path+'/'+img_name
        img = Image.open(picture_path)
        i = 0
        for annotation in ret_dic['annotations']:
            boxes = annotation['box']  #获取一个json文件中所有检测框
            # for box in boxes:
            box = tuple(boxes)
            img_size = img.size
            result = img.crop(box)  #遍历检测框的尺寸切割图片
            #Image._show(result)
            # 保存、重命名新切割出的图片‘/Volumes/硬盘/train_dataset_part1/image/000123/0_0.jpg’
            result.save(pictures_path + '/' + num + '_' + str(i) + '.jpg' )
            i = i+1

if __name__ == '__main__':
    path = "/Volumes/硬盘/train_dataset_part1/image_annotation"
    img_path = '/Volumes/硬盘/train_dataset_part1/image'
    files= os.listdir(path) #得到该路径下的所有文件名，即文件夹 000493 这个
    for file in files:
        if(file[0]=="."):
            continue
        jsons_path = path+"/"+file   #081009的json文件夹
        picture_path =img_path+"/"+file    #081009的image文件夹
        jsons = os.listdir(jsons_path)  # 得到该路径下的所有文件名，即文件 0.json, 1.json,2.json
        for _json in jsons:
            if (_json[0] == "."):
                continue
            json_path = jsons_path + "/" + _json
            # print(json_path)
            explain_json(json_path, picture_path)
