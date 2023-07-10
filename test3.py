from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

## 파일 실행폴더와 같은 경로에 chromedriver가 있을경우엔 parameter는 넣지 않아도됨 
driver = webdriver.Chrome()

driver.get('https://www.bifrostnetwork.com/stake')
time.sleep(3)
