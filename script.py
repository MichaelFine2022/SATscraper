from selenium import webdriver
from selenium.webdriver.chrome.service import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://satsuitequestionbank.collegeboard.org/")
time.sleep(2)
findQuestionsButton = driver.find_element(By.CLASS_NAME, "cb-btn cb-btn-black").click()
chooseAssessments = driver.find_element(By.ID,"selectAssessmentType").click()
chooseAssessments.select_by_value(99)
time.sleep(1)
selectType = driver.find_element(By.ID,"selectTestType").click()
selectType.select_by_value(1)
time.sleep(1)
checkbox = driver.find_element(By.ID,"apricot_check_128").click()
checkbox = driver.find_element(By.ID,"apricot_check_129").click()
checkbox = driver.find_element(By.ID,"apricot_check_130").click()
checkbox = driver.find_element(By.ID,"apricot_check_131").click()
time.sleep(1)
submit = driver.find_element(By.CLASS_NAME, "cb-btn square cb-roboto cb-btn-primary").click()
time.sleep(1)
driver.quit()