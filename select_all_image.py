import pymysql
import shutil
conn = pymysql.connect(
        host='localhost',
        user='root',
        password='vic915_love@163',
        db='platform_clothes',
        charset='utf8',
        # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
    )
try:
    with conn.cursor() as cursor:
        cursor.execute("select A.instance_id,img_name,label,B.img_id from item as A,item_image as B where A.instance_id = B.instance_id")
        label = [
            "短袖上衣","长袖上衣","短袖衬衫",
            "长袖衬衫","背心上衣","吊带上衣",
            "无袖上衣","短外套","短马甲",
            "长袖连衣裙","短袖连衣裙","无袖连衣裙",
            "长马甲","长外套","连体衣",
            "短裙","中等半身裙","长半身裙",
            "短裤","中裤","长裤","背带裤","古风"
        ]
        tmp = [[] for x in range(23)]
        for data in cursor.fetchall():
            img_data = list(data)
            # print(img_data[2])
            # print(img_data[3])
            for lab in label:
                if img_data[2] == lab:
                    newpath = "/Volumes/硬盘/clothes_image_all"+"/"+str(label.index(lab))+"_"+str(len(tmp[label.index(lab)]))+".jpg"
                    shutil.copyfile(img_data[3], newpath)
                    tmp[label.index(lab)].append(1)
                    # print(img_data)
except pymysql.Error as error:
    print(error)
finally:
    conn.close()



