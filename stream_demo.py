import cv2
import requests
from selenium import webdriver
from selenium import common
from selenium.webdriver.support.ui import Select
import urllib.request

class ImgLoader():
    def __init__(self):
        self.driver = webdriver.Edge("F:/2021spring/ece695i/yolo3-pytorch-master/msedgedriver.exe")
        self.driver.get("http://10.4.6.109")
        self.button_toggle = self.driver.find_element_by_id("toggle-stream")
        self.button_still = self.driver.find_element_by_id("get-still")
        self.select = Select(self.driver.find_element_by_id("framesize"))
        self.select.select_by_visible_text('UXGA(1600x1200)')

    def getImg(self):
        self.button_toggle.click()
        self.button_still.click()
        img = self.driver.find_element_by_id('stream')
        src = img.get_attribute('src')
        response = requests.get(src)
        if response.status_code == 200:
            with open("temp_img.jpg", 'wb') as f:
                f.write(response.content)
        return "temp_img.jpg"


if __name__ == "__main__":
    il = ImgLoader()
    il.getImg()