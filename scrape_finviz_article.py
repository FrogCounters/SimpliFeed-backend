import requests
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


import time
# from connect_db import *





class Scraper:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}
    
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url, headers=Scraper.headers)
    
    def getDoc(self):
        if not self.response.ok:
            print('Status code:', self.response.status_code)
            raise Exception('Failed to load page {}'.format(self.ur))
        page_content = self.response.text
        self.doc = BeautifulSoup(page_content, 'html.parser')
        return self.doc

    def getText(self):
        total_text = ""
        p = self.doc.find_all("p")
        for i in p:
            total_text += i.text + "\n"
        
        return total_text
    
    def _defaultParse(self):
        self.getDoc()
        self.getText()
    
    def parse(self):
        self._defaultParse()
    

class SeleniumScraper:

    @staticmethod
    def get_driver(url):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        # chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--start-fullscreen')
        # chrome_options.add_argument('--single-process')
        serv = Service(os.getcwd()+'/chromedriver')
        driver = webdriver.Chrome(options=chrome_options, service=serv) 
        driver.get(url)
        return driver
    
    
    def __init__(self, url, title=None, body=None, date=None):
        self.article_url = url
        self.driver = self.get_driver(self.article_url)
        self.article_body = body
        self.article_title = title
        self.article_date = date

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, value=xpath)
        except NoSuchElementException:
            return False
        return True

    def _getBody(self):
        total_text = ""
        ps = self.driver.find_elements(By.TAG_NAME, value='p')
        for p in ps:
            total_text += p.text + "\n"
        self.article_body = total_text
    
    def getBody(self):
        self._getBody()
        return self.article_body
    


class ScraperBloomberg(SeleniumScraper): #not functional

    def _getBody(self):
        self.article_body = "not implemented for bloomberg"

class ScraperReuters(SeleniumScraper):

    def _getBody(self):
        total_text = ""
        para_no = 0
        xpath = f"//p[@data-testid='paragraph-{para_no}']"
        while self.check_exists_by_xpath(xpath):
            reuters_para = self.driver.find_element(By.XPATH, value=xpath)
            total_text += reuters_para.text + "\n"
            para_no += 1
            xpath = f"//p[@data-testid='paragraph-{para_no}']"
            
        self.article_body = total_text
    
    # def _getTitle(self):

    #     xpath = '//h1[@data-testid="Heading"]'
    #     if self.check_exists_by_xpath(xpath):
    #         reuters_title = self.driver.find_element(By.XPATH, value=xpath)
    #         self.article_title = reuters_title.text

    