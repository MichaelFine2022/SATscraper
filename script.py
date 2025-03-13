from selenium import webdriver
from selenium.webdriver.chrome.service import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://satsuitequestionbank.collegeboard.org/")
findQuestionsButton = driver.find_element(By.CLASS_NAME, "cb-btn cb-btn-black").click()
chooseAssessments = driver.find_element(By.ID,"selectAssessmentType").click()

time.sleep(10)
driver.quit()