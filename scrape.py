import time
import numpy as np
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from config import url, infiniteScrollTimeout, username, password 

import csv

driver = webdriver.Chrome(ChromeDriverManager().install())

class Scrape:
    def __init__(self):
            self.options = self.browser_options()
            self.wait = WebDriverWait(driver, 30)
            driver.maximize_window()


    def browser_options(self):
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            return options


    def manipulate_string(self, string):
        # Save 70.0% on select products from JIUMUJIPU with promo code 70CC3G1M, through 2/20 while supplies last.
        # Delete the first 
        
        start = string.find('Save ') + 5
        end = string.find(' on select')
        returnString = string[start:end] + ','
        start = string.find('products from') + 14
        end = string.find(' with promo')
        returnString = returnString + string[start:end] + ','
        start = string.find('promo code ') + 11
        end = string.find(', through')
        returnString = returnString + string[start:end] + ','
        start = end + 10
        end = string.find(' while supplies')
        returnString = returnString + string[start:end]
        return returnString
        
    def login(self):
        print('Login')

        time.sleep(5)

        select_username = driver.find_element_by_xpath('//*[@id="ap_email"]')
        select_username.send_keys(username)

        select_password = driver.find_element_by_xpath('//*[@id="ap_password"]')
        select_password.send_keys(password)
        ## press ENTER key 
        select_password.send_keys(Keys.ENTER)
        error = "temp"
        if error is None:
            print("Login error!")
            
        time.sleep(5)
        print('Finished login')
        
    def scroll(self):
        prev_length = 0
        pause = 1
        timeout = infiniteScrollTimeout
        noChange = 0
        prevSource = driver.page_source
        currentSource = ''
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        while True:
            time.sleep(pause)
            currentSource = driver.page_source
            if prevSource != currentSource:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                noChange = 0
                time.sleep(3)
                prev_length = self.find_promo(prev_length)
            else:
                print('inc no change: %d' % noChange)
                noChange += 1
            if noChange == timeout:
                print('After %d second pause, we have reached the bottom' % timeout)
                break;
                
            prevSource = currentSource


    def find_promo(self, start_length):
    
        

        promo_box = driver.find_element_by_xpath('//*[@id="ac-promohub-mpc-content"]/div[1]/div[2]')
        promo_items = promo_box.find_elements_by_class_name('a-link-normal')
        for i in range (start_length, len(promo_items)):
            listingString = self.manipulate_string(promo_items[i].text)
            listingString = listingString.split(',')
            with open('data.csv', mode='a') as data:
                dataWriter = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                dataWriter.writerow([listingString[1],listingString[0],listingString[3],listingString[2],promo_items[i].get_attribute('href')])
        return len(promo_items)
           
    def run(self, url):
        with open('data.csv', mode='a') as data:
            dataWriter = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            dataWriter.writerow(['Company Name','Discount Percentage','End Date','Promo Code','Link'])
            
        driver.get(url)
        
        self.login()
        
        time.sleep(10)
        
        driver.find_element_by_xpath('//*[@id="ac-promohub-promo-filter"]/div/div[2]/span/div/label/i').click()
        time.sleep(1)
        self.scroll()

        print('Found and wrote %d promo items' % len(promo_items))

        
bot = Scrape()
bot.run(url)
