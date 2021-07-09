#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import os
import json
from PIL import Image

def explain_json(cur,conn,path,pictures_path):
    with open(path, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        #print(type(ret_dic)) # 结果 <class 'dict'>
        #print(ret_dic)
        item_id = ret_dic['item_id']
        img_name = ret_dic['img_name']
        picture_path = pictures_path+'/'+img_name
        i=0
        num = img_name[0]
        for annotation in ret_dic['annotations']:
            viewpoint = annotation['viewpoint']
            instance_id = annotation['instance_id']
            label = annotation['label']
            box = annotation['box']
            display = annotation['display']
            new_picture_path = cut_picture(box,picture_path,pictures_path,i,num)
            if(instance_id != 0):
                if isExit(cur,instance_id):
                    insertToItem(cur,conn,instance_id,item_id,label)
                insertToItemimage(cur,conn,instance_id,img_name,viewpoint,display,box,new_picture_path)
           #print(item_id,viewpoint,instance_id,label,box,display,img_name,picture_path) #拿到数据
            i+=1

def cut_picture(boxes,picture_path,pictures_path,i,num):
    img = Image.open(picture_path)
    box = tuple(boxes)
    result = img.crop(box)
   # Image._show(result)
    new_picture_path=pictures_path + '/' + num + '_' + str(i) + '.jpg'
    result.save(pictures_path + '/' + num + '_' + str(i) + '.jpg')
    return new_picture_path

def conn():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        db='platform_clothes',
        charset='utf8',
        # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
    )
    cur = conn.cursor()
    return cur,conn

def insertToItem(cur,conn,instance_id,item_id,label):
    try:
        insert_sqli = "insert into item(instance_id,item_id,label) values('%s','%s','%s')"%(instance_id,item_id,label)
        cur.execute(insert_sqli)
    except Exception as e:
        print("插入数据失败:", e)
    else:
        # 如果是插入数据， 一定要提交数据， 不然数据库中找不到要插入的数据;
        conn.commit()
        #print("插入数据成功;")

def insertToItemimage(cur,conn,instance_id,img_name,viewpoint,display,box,img_id):
    try:
        insert_sqli = "insert into item_image(instance_id,img_name,viewpoint,display,box,img_id) values('%s','%s','%s','%s','%s','%s')"%(instance_id,img_name,viewpoint,display,box,img_id)
        #print(insert_sqli)
        cur.execute(insert_sqli)
    except Exception as e:
        print("插入数据失败:", e)
    else:
        # 如果是插入数据， 一定要提交数据， 不然数据库中找不到要插入的数据;
        conn.commit()
       #print("插入数据成功;")

def isExit(cur,instance_id):
    sqli = "select * from item where instance_id ='%s'" % instance_id
    result = cur.execute(sqli)  # 默认不返回查询结果集， 返回数据记录数。
    if result == 0:
        return True
    return False

if __name__ == '__main__':
    cur,conn=conn()
    path = "/Volumes/硬盘/train_dataset_part2/image_annotation"
    img_path = '/Volumes/硬盘/train_dataset_part2/image'
    files= os.listdir(path) #得到该路径下怼所有文件名，即文件夹 000493 这个
    # print(files)
    for file in files:
        if(file[0]=="."):
            continue
        jsons_path = path+"/"+file
        picture_path =img_path+"/"+file
        jsons = os.listdir(jsons_path) #得到该路径下怼所有文件名，即文件 0.json, 1.json,2.json
        # print(jsons)
        for _json in jsons:
            if (_json[0] == "."):
                continue
            json_path = jsons_path + "/" + _json
            #print(json_path)
            explain_json(cur,conn,json_path,picture_path)
