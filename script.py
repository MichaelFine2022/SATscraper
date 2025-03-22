import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://satsuitequestionbank.collegeboard.org/")
#its a python hashset lmao
visited = set()
def scrapeFromID(element, writer):
    try:
        element_id = element.get_attribute('id')
        element.click()
        
        # Wait until elements are visible instead of using sleep
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'prompt.cb-margin-top-32')))

        upperPrompt = driver.find_element(By.CLASS_NAME, 'prompt.cb-margin-top-32')
        lowerPrompt = driver.find_element(By.CLASS_NAME, 'question.cb-margin-top-16')

        upperAnswer = driver.find_element(By.CLASS_NAME, 'correct-answer.cb-margin-top-32')
        lowerAnswer = driver.find_element(By.CLASS_NAME, 'rationale.cb-margin-top-16')
        
        correctAnswerString = upperAnswer.find_element(By.TAG_NAME, 'h6')
        correctAnswerChar = upperAnswer.find_element(By.TAG_NAME, 'p')

        correctAnswer = correctAnswerString.text + correctAnswerChar.text
        combinedQuestion = upperPrompt.text + '\n' + lowerPrompt.text
        combinedAnswer = correctAnswer + '\n' + lowerAnswer.text

        writer.writerow([element_id, combinedQuestion, combinedAnswer])

        # Close the question popup
        exitButton = driver.find_element(By.CLASS_NAME, 'cb-glyph.cb-x-mark')
        exitButton.click()
        
    except Exception as e:
        print(f"Error scraping element {element_id}: {e}")

def getIDs(writer):
    idSet = driver.find_elements(By.CSS_SELECTOR, 'button.cb-btn.square.cb-roboto.cb-btn-naked.view-question-button')
    for element in idSet:
        try:
            question_id = element.text.strip()
            
            if question_id in visited:
                continue
            
            visited.add(question_id)
            scrapeFromID(element, writer)
            
            # Wait for page stability before next click
            WebDriverWait(driver, 2).until(EC.staleness_of(element))
        
        except Exception as e:
            print(f"Error processing question {question_id}: {e}")

def startUp(): 
    try:
        # Wait for the button and click it
        findQuestionsButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cb-btn.cb-btn-black"))
        )
        findQuestionsButton.click()

        # Wait for dropdown and select value
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "selectAssessmentType")))
        chooseAssessments = Select(driver.find_element(By.ID, "selectAssessmentType"))
        chooseAssessments.select_by_value("99")

        selectType = Select(driver.find_element(By.ID, "selectTestType"))
        selectType.select_by_value("1")

        # Check required checkboxes
        for checkbox_id in ["apricot_check_128", "apricot_check_129", "apricot_check_130", "apricot_check_131"]:
            checkbox = driver.find_element(By.ID, checkbox_id)
            if not checkbox.is_selected():
                checkbox.click()

        # Submit button click
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cb-btn.square.cb-roboto.cb-btn-primary"))
        )
        submit_button.click()
    
    except Exception as e:
        print(f"Error during startup: {e}")

#do you think this stuff counts as CP?
startUp()
with open('output.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "question", "answer"])
    # Write the header
    writer.writeheader()
getIDs(writer)