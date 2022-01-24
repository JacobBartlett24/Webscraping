from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


class vinyl_object():
    
    def __init__(self, title, artist, label, price):
        self.title = title
        self.artist = artist
        self.price = price
        
    def print_vinyl_info(self):
        print("title = " + self.title + "\nartist = " + self.artist + "\nprice = "+ self.price + "\n")

def write_to_csv(vinyl):

    row = [vinyl.artist,vinyl.title,vinyl.price, "Amazon Title"]
    file_name = "vinyldataamazon.csv"
    csvfile = open(file_name, 'a+',newline = '',encoding="utf-8")
    csvwriter = csv.writer(csvfile, dialect='excel')
    csvwriter.writerow(row)

def format_artist_string(artist_name):
    
    artist_name = artist_name.split ('|')
    formatted_arist_name = artist_name[0].split(' ',1)
    if(len(formatted_arist_name)>1):
        return formatted_arist_name[1]

    else:
        return "ErrorPlaceHolder"

def format_text(vinyl_info):

    found = 0
    vinyl_info = vinyl_info.split('\n')
    cur_vinyl = vinyl_object
    
    if(vinyl_info[0] != "Best Seller"):

        cur_vinyl.title = vinyl_info[0]
        cur_vinyl.artist = vinyl_info[1]
    
    
    else:

        cur_vinyl.title = vinyl_info[1]
        cur_vinyl.artist = vinyl_info[2]

    for i in range(len(vinyl_info)):
        
        if(vinyl_info[i].rfind('$') == 0 and found != -1):

            complete_price = vinyl_info[i] + "." + vinyl_info[i+1]
            cur_vinyl.price = complete_price
            found = -1

    cur_vinyl.artist = format_artist_string(cur_vinyl.artist)
    write_to_csv(cur_vinyl)

    
class TargetClient(object):
    def __init__(self):

        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)
        self.base_url = 'https://www.amazon.com/b?ie=UTF8&node=14772275011'
        self.driver.get(self.base_url)
        time.sleep(2)
        
    def search_website(self):
        
        self.driver.find_element(By.CSS_SELECTOR,"[aria-label = 'New releases']").click()

    def scrape_script(self):

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[data-component-type='s-search-result']")))
        vinyls = self.driver.find_elements(By.CSS_SELECTOR,"[data-component-type='s-search-result']")
        lengthofvinyls = str(len(vinyls))

        if(lengthofvinyls != 16):
            time.sleep(3)
            vinyls = self.driver.find_elements(By.CSS_SELECTOR,"[data-component-type='s-search-result']")
            lengthofvinyls = str(len(vinyls))

        for x in vinyls:
            format_text(x.text)
            
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")))
        self.driver.find_element(By.CLASS_NAME, "s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator").click()
        self.scrape_script()


def main():
    targ = TargetClient()
    targ.search_website()
    targ.scrape_script()
    time.sleep(10)
    

if __name__ == '__main__':
    main()