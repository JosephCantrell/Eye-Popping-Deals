import time
import numpy as np
import argparse
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import winsound
from config import url, infiniteScrollTimeout, username, password 

import csv

driver = webdriver.Chrome(ChromeDriverManager().install())

class Scrape:
    def __init__(self, args):
            self.options = self.browser_options()
            self.wait = WebDriverWait(driver, 30)
            driver.maximize_window()
            self.args = args


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
        # Ugly function but it gets the information that we need. takes into consideration that we might have a company name that has multiple spaces
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
        # Find the email element and put the stored email in the text field
        select_username = driver.find_element_by_xpath('//*[@id="ap_email"]')
        select_username.send_keys(username)
        
        currentURL = driver.current_url

        # Find the Password element and put the stored password in the text field
        select_password = driver.find_element_by_xpath('//*[@id="ap_password"]')
        select_password.send_keys(password)
        ## press ENTER key 
        select_password.send_keys(Keys.ENTER)
        
        time.sleep(5)
        
        
        print('Finished login')
        
    def check_target_url(self, targetURL):
        if driver.current_url == targetURL:
            return True
        return False
        
    def scroll(self):
        # Value that is passed to find_promo
        prev_length = 0
        # How long do we pause between scroll checks (default 1s)
        pause = 1
        # Get the timeout from the config file
        timeout = infiniteScrollTimeout
        # The counter that counts how many long it has been since the page source hasnt changed
        noChange = 0
        
        # Changed from page source comparing to comparing the length of the elements that we are looking for. 
        # Find the promo_box and get the number of elements on screen.
        promo_box = driver.find_element_by_xpath('//*[@id="ac-promohub-mpc-content"]/div[1]/div[2]')
        prev_element_len = len(promo_box.find_elements_by_class_name('a-link-normal'))
        # Init current source to empty
        current_element_len = ''
        # Delay just incase
        time.sleep(5)
        # Scroll to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        while True:
            # Do the initial pause 
            time.sleep(pause)
            
            # Changed from page source comparing to comparing the length of the elements that we are looking for.
            # Have to find the promo_box each time
            promo_box = driver.find_element_by_xpath('//*[@id="ac-promohub-mpc-content"]/div[1]/div[2]')
            current_element_len = len(promo_box.find_elements_by_class_name('a-link-normal'))
            if prev_element_len != current_element_len:
                # Our number of elements doesnt match, the infinite scrolling added more items, so scroll to the bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Reset the counter
                noChange = 0
                # Sleep for 1 second
                time.sleep(1)
                # Set the previous length (number of code elements on screen currently) to the return value of find_promo
                prev_length = self.find_promo(prev_length)
                # Print out how many we have found while actively searching
                print('Found and wrote %d promo items' % prev_length)
            else:
                # There has been no change detected, start incrementing the counter
                print('No New Items in %d seconds' % noChange)
                noChange += 1
            if noChange == timeout:
                # If we detected no change for the timeout time, exit the loop and quit the code
                print('After %d second pause, we have reached the bottom' % timeout)
                break;
                
            # Set the previous length to the current length
            prev_element_len = current_element_len


    def find_promo(self, start_length):
    
        
        # Only search for promos in the promo box. There are other elements that have the same class name, and they can throw the code off
        promo_box = driver.find_element_by_xpath('//*[@id="ac-promohub-mpc-content"]/div[1]/div[2]')
        # This is the elements that we need, it has the information required
        promo_items = promo_box.find_elements_by_class_name('a-link-normal')
        for i in range (start_length, len(promo_items)):
            # Get the text of the promo item and manipulate it
            listingString = self.manipulate_string(promo_items[i].text)
            # Split the returned string into an array based off of ','
            listingString = listingString.split(',')
            # Open the data.csv and write the data points.
            # listingString[1] = Company Name
            # listingString[0] = Discount Percentage
            # listingString[3] = End Date
            # listingString[2] = Discount Code
            # Href is the link to the items
            with open('data.csv', mode='a') as data:
                dataWriter = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                dataWriter.writerow([listingString[1],listingString[0],listingString[3],listingString[2],promo_items[i].get_attribute('href')])
        # Return the length of our promo items. Determines the starting position of the next call
        return len(promo_items)
           
    def run(self, url):
        # Open and write the headers to the file. Currently in append mode to not override the old data.
        with open('data.csv', mode='a') as data:
            dataWriter = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            dataWriter.writerow(['Company Name','Discount Percentage','End Date','Promo Code','Link'])
        # Set the url
        driver.get(url)
        # Login
        self.login()
        # Sleep for 10 seconds
        time.sleep(10)
        # Click on upcoming deals checkmark
        if args.upcoming:
            driver.find_element_by_xpath('//*[@id="ac-promohub-promo-filter"]/div/div[2]/span/div/label/i').click()
            time.sleep(1)
        # Start scrolling
        self.scroll()

        


parser = argparse.ArgumentParser(description='Linkedin Automatic Job Applications')
parser.add_argument('-u','--upcoming', help='Enable upcoming deals', required=False, action='store_true',default=False)
args = parser.parse_args()

        
bot = Scrape(args)
bot.run(url)
