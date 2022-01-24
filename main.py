import threading
import time
import amazon_webscraper
import target_webscraper

firstThread = threading.Thread(target = amazon_webscraper.main).start()
time.sleep(1)
secondThread = threading.Thread(target = target_webscraper.main).start()

print("done")