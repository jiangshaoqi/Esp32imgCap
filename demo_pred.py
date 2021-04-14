from PIL import Image
from yolo import YOLO
from yolo_sub import YOLO_sub
import stream_demo
from stream_demo import ImgLoader

yolo_person = YOLO()
yolo_mask = YOLO_sub()
iloader = ImgLoader()

while True:
    file_name = iloader.getImg()
    try:
        image = Image.open(file_name)
    except:
        print('Open Error! Try again!')
        continue
    else:
        person_image, person_list = yolo_person.detect_image(image)
        person_image.show()
        if not person_list:
            temp_img = yolo_mask.detect_image(image)
            temp_img.show()
        else:
            image = Image.open(img)
            for each_person in person_list:
                top, left, bottom, right = each_person[0], each_person[1], each_person[2], each_person[3]
                face_img = image.crop((left, top, right, bottom))
                temp_img = yolo_mask.detect_image(face_img)
                temp_img.show()