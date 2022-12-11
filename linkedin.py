from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from halo import Halo
import warnings

warnings.filterwarnings('ignore')  #arrreglar los warnings

class Scraper(object):
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("window-size=1120x550")
        self.driver = webdriver.Chrome(
            executable_path=r"/usr/bin/chromedriver", options=options)
        self.spinner = Halo(text='Obteniendo contactos que no te siguen...', spinner='shark')
        load_dotenv()
        
        
    def scrape(self):
        self.driver.get("https:linkedin.com")
        username = self.driver.find_element("xpath","//*[@id=\"session_key\"]")
        
        usnm = os.getenv('EMAIL')#input("Please enter your email: ")
        username.send_keys(str(usnm))
        password = self.driver.find_element("xpath", "//*[@id=\"session_password\"]")
        pwd = os.getenv('PASSWORD') #input("Please enter your password: ")
        password.send_keys(str(pwd))
        sleep(5)
        self.driver.find_element("xpath", "//*[@id=\"main-content\"]/section[1]/div/div/form/button").click()
        sleep(5)
    
    def steps(self, link):
        
        self.driver.get(link)
        sleep(2)
        
        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        
        s = BeautifulSoup(self.driver.page_source, "html.parser")
        snippet = s.find_all('h3')
        contacts_list = []
        
        for element in snippet:
            contact = (element.text)
            contacts_list.append(str(contact).strip())
        return contacts_list
        
        
    def get_uncommon(self, followers_contacts_list, following_contacts_list):
        uncommon_contact_list = []
        for contact in following_contacts_list:
            if contact not in followers_contacts_list:
                uncommon_contact_list.append(contact)
        return uncommon_contact_list
        
        
if __name__ == '__main__':
    fwrs_link = "https://www.linkedin.com/feed/followers/"
    fwing_link = "https://www.linkedin.com/feed/following/?filterType=connection"
    scraper = Scraper()
    scraper.spinner.start()
    scraper.scrape()
    fwrs_contact_list = scraper.steps(fwrs_link)
    fwing_contact_list = scraper.steps(fwing_link)
    uncommon_contact_list = scraper.get_uncommon(fwrs_contact_list, fwing_contact_list)
    scraper.spinner.stop()
    print(f"\n{uncommon_contact_list}")
