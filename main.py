from queue import Empty
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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
    if(hasattr(vinyl,'price')):
        row = [vinyl.artist,vinyl.title,vinyl.price,vinyl.label]
    else: row = [vinyl.artist,vinyl.title,'0',vinyl.label]
    file_name = "vinyldata.csv"
    csvfile = open(file_name, 'a+')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(row)
    csvfile.close()
    


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
    next_page = driver.find_element(By.XPATH, "//*[@id='pageBodyContainer']/div[1]/div/div[4]/div/div[1]/div[2]/div/div[2]/div/div/div[3]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);",next_page)
    time.sleep(2)
    driver.execute_script("arguments[0].click();",next_page)

def scrape_script(driver, vinyls):

    for x in vinyls:
        save_valuable_values(x.text)
        if(x.text) == (''):
            driver.execute_script("arguments[0].scrollIntoView(true);",x)
            vinyls = driver.find_elements(By.XPATH, "//div[@class='styles__StyledCol-sc-fw90uk-0 dNNWBw']")
            time.sleep(2)
    goto_nextpage(driver)
    time.sleep(10)
    vinyls = driver.find_elements(By.XPATH, "//div[@class='styles__StyledCol-sc-fw90uk-0 dNNWBw']")
    scrape_script(driver,vinyls)


PATH = "~/home/screenname21/repos/dependencies/chromedriver_linux64.zip"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.target.com')

driver.maximize_window()

search = driver.find_element(By.XPATH,"//input[@id='search']").send_keys("vinyls")
search = driver.find_element(By.XPATH,"//input[@id='search']").send_keys(Keys.RETURN)
time.sleep(2)

vinyls = driver.find_elements(By.XPATH, "//div[@class='styles__StyledCol-sc-fw90uk-0 dNNWBw']")

time.sleep(1.5)

scrape_script(driver, vinyls)

