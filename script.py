from selenium import webdriver     

import time 
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
 
driver = webdriver.Chrome() 
driver.get('https://satsuitequestionbank.collegeboard.org/digital/search')

visited = set()

def startUp():
    time.sleep(6)

    print('Clicking assessment')
    assessmentSelection = Select(driver.find_element(By.ID, 'selectAssessmentType'))
    assessmentSelection.select_by_visible_text('SAT')
    # sets it to SAT 

    testSelection = Select(driver.find_element(By.ID, 'selectTestType'))
    testSelection.select_by_visible_text('Reading and Writing')

    time.sleep(10)
    print("Selecting domain scores")
    time.sleep(10)
    boxInformationandIdea = driver.find_element(By.ID, "apricot_check_2")
    boxCraftAndStructure = driver.find_element(By.ID, "apricot_check_3")
    boxExpression = driver.find_element(By.ID, "apricot_check_4")
    boxStandardEnglish = driver.find_element(By.ID, "apricot_check_5")

    boxInformationandIdea.click()
    boxCraftAndStructure.click()
    boxExpression.click()
    boxStandardEnglish.click()

    time.sleep(1)

    firstSearch = driver.find_element(By.CSS_SELECTOR, 'button.cb-btn:nth-child(2)')
    firstSearch.click()

    time.sleep(10)

def getIDs(writer):
    idSet = driver.find_elements(By.CSS_SELECTOR, 'button.cb-btn.square.cb-roboto.cb-btn-naked.view-question-button')
    print("getting IDs")
    print(len(idSet))
    for element in idSet:
            print("Current element " + element.text)
            
            if (visited.__contains__(element.text)):
                continue
            else:
                visited.add(element.text)
                scrapeFromID(element, writer)
                time.sleep(2)

def scrapeFromID(element, curWriter):
    element_id = element.get_attribute('id')
    element.click()

    time.sleep(20)
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

    type = driver.find_element(By.XPATH, '//div[@id="question-modal"]//div[@class="question-detail-info"]/div/div[4]/div').text
    toWrite = [element_id, type, combinedQuestion, combinedAnswer]

    with open('output.csv', mode='a', newline='', encoding='utf-8') as file:
        
        writer = csv.writer(file)
        writer.writerow(toWrite)

    exitButton = driver.find_element(By.CLASS_NAME, 'cb-glyph.cb-x-mark')
    exitButton.click()

if __name__ == "__main__":
    startUp()
    with open('output.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id","type", "question", "answer"])
        
        # Write the header
        writer.writeheader()
    while (True):
        time.sleep(5)
        getIDs(writer)
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cb-btn.cb-btn-square.cb-btn-greyscale")))
        if buttons:
            last_button = buttons[-1]
            driver.execute_script("arguments[0].scrollIntoView(true);", last_button) 
            driver.execute_script("arguments[0].click();", last_button)     
