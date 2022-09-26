from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class vinyl_object():
    
    def __init__(self, title, artist, label, price):
        self.title = title
        self.artist = artist
        self.price = price
        self.label = label
        
    def print_vinyl_info(self):
        print("title = " + self.title + "\nartist = " + self.artist + "\nprice = "+ self.price + "\n" "label = "+ self.label + "\n")

def write_to_csv(vinyl):

    row = [vinyl.artist,vinyl.title,vinyl.price,vinyl.label]
    file_name = "vinyldataamazon.csv"
    csvfile = open(file_name, 'a+',newline = '')
    csvwriter = csv.writer(csvfile, dialect='excel')
    csvwriter.writerow(row)

def format_text(vinyl_info):

    cur_vinyl = vinyl_object
    vinyl_info = vinyl_info.split('\n')
    set_current_vinyls_attributes(vinyl_info, cur_vinyl)
    write_to_csv(cur_vinyl)

def set_current_vinyls_attributes(vinyl_info, cur_vinyl):
    
    artist_and_title = vinyl_info[0].split(' - ')
    if(len(artist_and_title) == 2):
        cur_vinyl.artist = artist_and_title[0]
        cur_vinyl.title  = artist_and_title[1]
    if(len(vinyl_info) > 2):
        cur_vinyl.label  = vinyl_info[1]
    for i in range(len(vinyl_info)):
        if(vinyl_info[i].rfind('$') == 0):
            cur_vinyl.price = vinyl_info[i]

class TargetClient(object):

    def __init__(self):

        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)
        self.base_url = 'https://www.target.com/'
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        time.sleep(2)

    def search_site(self):
        self.driver.find_element(By.XPATH,"//input[@id='search']").send_keys("vinyls")
        self.driver.find_element(By.XPATH,"//input[@id='search']").send_keys(Keys.RETURN)

    def goto_nextpage(self):

        next_page = self.driver.find_element(By.XPATH, "//*[@id='pageBodyContainer']/div[1]/div/div[4]/div/div[1]/div[2]/div/div[2]/div/div/div[3]/button/span/div/svg']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);",next_page)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pageBodyContainer']/div[1]/div/div[4]/div/div[1]/div[2]/div/div[2]/div/div/div[3]/button/span/div/svg")))
        self.driver.execute_script("arguments[0].click();",next_page)


    def scrape_script(self):

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@data-test='list-entry-product-card']")))
        vinyls = self.driver.find_elements(By.XPATH, "//li[@data-test='list-entry-product-card']")

        for i in range(len(vinyls)):

            if(vinyls[i].text):
                self.driver.execute_script("arguments[0].scrollIntoView();", vinyls[i])
                #vinyls = self.driver.find_elements(By.XPATH, "//li[@data-test='list-entry-product-card']")
            format_text(vinyls[i].text)

        self.goto_nextpage()
        self.scrape_script()            
        
            
        

def main():
    targ = TargetClient()
    targ.search_site()
    targ.scrape_script()
    time.sleep(10)
    

if __name__ == '__main__':
    main()