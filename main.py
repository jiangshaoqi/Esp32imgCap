import cv2
import requests
from selenium import webdriver
from selenium import common
import urllib.request


if __name__ == "__main__":
    driver = webdriver.Edge("C:/Users/jiang/PycharmProjects/videoDemo/edgedriver_win64/msedgedriver.exe")
    # cnt = False
    # while not cnt:
    #     try:
    #        driver.get("http://10.4.6.109")
    #    except common.exceptions.WebDriverException:
    #        continue
    #    else:
    #        cnt = True
    driver.get("http://10.4.6.109")
    button_toggle = driver.find_element_by_id("toggle-stream")
    button_still = driver.find_element_by_id("get-still")
    for i in range(5):
        button_toggle.click()
        button_still.click()
        img = driver.find_element_by_id('stream')
        src = img.get_attribute('src')
        print(src)
        response = requests.get(src)
        if response.status_code == 200:
            with open("temp.jpg", 'wb') as f:
                f.write(response.content)
            img = cv2.imread("temp.jpg")
            cv2.imshow("window", img)
            cv2.waitKey(5000)
            cv2.destroyAllWindows()
    driver.close()
