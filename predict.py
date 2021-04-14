'''
predict.py有几个注意点
1、无法进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用Image.open打开图片文件进行预测。
2、如果想要保存，利用r_image.save("img.jpg")即可保存。
3、如果想要获得框的坐标，可以进入detect_image函数，读取top,left,bottom,right这四个值。
4、如果想要截取下目标，可以利用获取到的top,left,bottom,right这四个值在原图上利用矩阵的方式进行截取。
'''
from PIL import Image
from yolo import YOLO
from yolo_sub import YOLO_sub
from peopledense import DensityDetector

yolo_person = YOLO()
dense_det = DensityDetector()
yolo_mask = YOLO_sub()

while True:
    img = input('Input image filename:')
    try:
        image = Image.open(img)
    except:
        print('Open Error! Try again!')
        continue
    else:
        person_image, person_list = yolo_person.detect_image(image)
        print(person_list)
        dense_list = dense_det.checkDensity(person_list)
        print(dense_list)
        # person_image.show()

        if not person_list:
            pass
        else:
            image = Image.open(img)
            mask_list = []
            for each_person in person_list:
                top, left, bottom, right = each_person[0], each_person[1], each_person[2], each_person[3]
                face_img = image.crop((left, top, right, bottom))
                temp_img, is_mask = yolo_mask.detect_image(face_img)
                mask_list.append(is_mask)
                # temp_img.show()
            print(mask_list)
