import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://satsuitequestionbank.collegeboard.org/")
#its a python hashset lmao
visited = set()
def scrapeFromID(element, writer):
    element_id = element.get_attribute('id')
    element.click()

    time.sleep(5)
    print("Finding elements")
    upperPrompt = driver.find_element(By.CLASS_NAME, 'prompt.cb-margin-top-32')
    lowerPrompt = driver.find_element(By.CLASS_NAME, 'question.cb-margin-top-16')

    upperAnswer = driver.find_element(By.CLASS_NAME, 'correct-answer.cb-margin-top-32')
    lowerAnswer = driver.find_element(By.CLASS_NAME, 'rationale.cb-margin-top-16')
    
    correctAnswerString = upperAnswer.find_element(By.TAG_NAME, 'h6')
    correctAnswerChar = upperAnswer.find_element(By.TAG_NAME, 'p')

    correctAnswer = correctAnswerString.text + correctAnswerChar.text

    combinedQuestion = upperPrompt.text + '\n' + lowerPrompt.text

    combinedAnswer = correctAnswer + '\n' + lowerAnswer.text

    combinedQuestion = combinedQuestion
    combinedAnswer = combinedAnswer

    toWrite = [element_id, combinedQuestion, combinedAnswer]

    with open('output.csv', mode='a', newline='', encoding='utf-8') as file:
        
        writer = csv.writer(file)
        writer.writerow(toWrite)

    exitButton = driver.find_element(By.CLASS_NAME, 'cb-glyph.cb-x-mark')
    exitButton.click()
def getIDs(writer):
    idSet = driver.find_elements(By.CSS_SELECTOR, 'button.cb-btn.square.cb-roboto.cb-btn-naked.view-question-button')
    for element in idSet:
            print("Current element " + element.text)
            
            if (visited.__contains__(element.text)):
                continue
            else:
                visited.add(element.text)
                scrapeFromID(element, writer)
                time.sleep(2)
def startUp(): 
    time.sleep(10)
    try:
        tfindQuestionsButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cb-btn.cb-btn-black"))
        )
        tfindQuestionsButton.click()
    except Exception as e:
        print(f"Error finding the element: {e}")
        return
    time.sleep(10)
    try:
        chooseAssessments = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "selectAssessmentType"))
        )
        chooseAssessments.click()
    except Exception as e:
        print(f"Error finding the element: {e}")
        return
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
    time.sleep(10)
#do you think this stuff counts as CP?
startUp()
with open('output.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "question", "answer"])
    # Write the header
    writer.writeheader()
getIDs(writer)