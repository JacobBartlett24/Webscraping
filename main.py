from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv

class vinyl_object():
    
    def __init__(self, title, artist, label, price):
        self.title = title
        self.artist = artist
        self.label = label
        self.price = price
        
    def print_vinyl_info(vinyl):
        print("title = " + vinyl.title + "\nartist = " + vinyl.artist + "\nlabel = "+ vinyl.label + "\nprice = "+ vinyl.price + "\n")
    
def write_to_csv(vinyl):

    row = [vinyl.artist,vinyl.title,vinyl.price,vinyl.label]
    file_name = "vinyl data.csv"
    csvfile = open(file_name, 'a+',newline = '')
    csvwriter = csv.writer(csvfile, dialect='excel')
    csvwriter.writerow(row)


def save_valuable_values(vinyl):

    vinyl = vinyl.split('\n')
    current_vinyl = vinyl_object
    for i in range(len(vinyl)):

        if(i == 0):

            arist_name_and_title = vinyl[i].split('-')

            if(len(arist_name_and_title) != 1):

                current_vinyl.artist = arist_name_and_title[0]
                current_vinyl.title = arist_name_and_title[1]

        elif(i == 1):

            current_vinyl.label = vinyl[i]
            
        elif(vinyl[i].rfind('$') == 0):

            current_vinyl.price = vinyl[i]

    write_to_csv(current_vinyl)
    

def goto_nextpage(driver):
    next_page = driver.find_element(By.XPATH, "//a[@aria-label='next page']")
    driver.execute_script("arguments[0].scrollIntoView(true);",next_page)
    time.sleep(2)
    driver.execute_script("arguments[0].click();",next_page)

def scrape_script(driver, vinyls):

    for x in vinyls:
        save_valuable_values(x.text)
        if(x.text) == (''):
            driver.execute_script("arguments[0].scrollIntoView(true);",x)
            vinyls = driver.find_elements(By.XPATH, "//li[@data-test='list-entry-product-card']")
            time.sleep(2)
    goto_nextpage(driver)
    time.sleep(4)
    vinyls = driver.find_elements(By.XPATH, "//li[@data-test='list-entry-product-card']")
    scrape_script(driver,vinyls)


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('https://www.target.com')

driver.maximize_window()

search = driver.find_element(By.XPATH,"//input[@id='search']").send_keys("vinyls")
search = driver.find_element(By.XPATH,"//input[@id='search']").send_keys(Keys.RETURN)
time.sleep (2)

vinyls = driver.find_elements(By.XPATH, "//li[@data-test='list-entry-product-card']")
time.sleep(1.5)

scrape_script(driver, vinyls)

