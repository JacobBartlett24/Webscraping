from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
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

    row = [vinyl.artist,vinyl.title,vinyl.price]
    file_name = "vinyldatauo.csv"
    csvfile = open(file_name, 'a+',newline = '')
    csvwriter = csv.writer(csvfile, dialect='excel')
    csvwriter.writerow(row)

def format_title_and_artist(line,cur_vinyl):
    line = line.split(' - ')
    cur_vinyl.artist = line[0]
    cur_vinyl.title = line[1]
    
class TargetClient(object):

    def __init__(self):

        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)
        self.base_url = 'https://www.urbanoutfitters.com/vinyl-records'
        self.driver.get(self.base_url)
        time.sleep(2)

    def format_text(self,vinyl_info):
        vinyl_info_text = vinyl_info.text
        vinyl_info_text = vinyl_info_text.split('\n')
        cur_vinyl = vinyl_object
        format_title_and_artist(vinyl_info_text[0],cur_vinyl)

        if(len(vinyl_info_text) != 2):
            self.driver.execute_script("arguments[0].scrollIntoView();", vinyl_info)
            price = vinyl_info.find_element(By.CSS_SELECTOR,"[class='c-pwa-product-price__current']")
            cur_vinyl.price = price.text
        else:
            print(vinyl_info_text[2])

        write_to_csv(cur_vinyl)
    

    def scrape_script(self):

        time.sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class='c-pwa-tile-grid-inner']")))
        ##WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class='c-pwa-product-price__current']")))
        vinyls = self.driver.find_elements(By.CSS_SELECTOR,"[class='c-pwa-tile-grid-inner']")
        length_of_vinyl = str(len(vinyls))

        for i in range(len(vinyls)):
            self.format_text(vinyls[i])

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID,"onetrust-accept-btn-handler")))
        self.driver.find_element(By.ID,"onetrust-accept-btn-handler").click()

        #WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[class='c-pwa-button-arrow__icon c-pwa-button-arrow__icon--right c-pwa-button-arrow__icon--pagination c-pwa-button-arrow__icon c-pwa-icon']")))
        #next_page = self.driver.find_element(By.CSS_SELECTOR,"[aria-label='Next']")
        #self.driver.execute_script("window.scrollBy(0,1000)")
        next_page = self.driver.find_element(By.CSS_SELECTOR,"[aria-label='Next']").click()
        self.scrape_script()


def main():
    targ = TargetClient()
    time.sleep(10)
    targ.scrape_script()
    time.sleep(10)


if __name__ == '__main__':
    main()