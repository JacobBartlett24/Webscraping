import requests
import csv
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import html

PATH = "C:\Program Files (x86)\chromedriver.exe"

base_url = 'https://www.target.com'

html_content = requests.get(base_url).text

soup = BeautifulSoup(html_content, "lxml")


print(search)


