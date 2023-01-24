from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


"""
This script provides a base class with the general utility for any Selenium based web scraping needed for the simplifeed project.
It is not intended to be used directly but instead inherited by a child classes that accounts for any major publisher's differences in website formatting.
Selenium is used as many of the websites require javascript files to be run before displaying properly.
"""
class SeleniumScraper:
    
    """
    The driver is used to load the javascript on websites as if a real user was using it
    """
    @staticmethod
    def get_driver(url):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
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

    """
    The default _getBody should be modified in most inherited classes based on the respective publisher's website format
    """
    
    def _getBody(self):
        total_text = ""
        ps = self.driver.find_elements(By.TAG_NAME, value='p')
        for p in ps:
            total_text += p.text + "\n"
        self.article_body = total_text
    
    # this is intended to be the public method that the main scraping script calls
    def getBody(self):
        self._getBody()
        return self.article_body

    """
    Utility method to check that the XPath intended for use actually exists in the current context.
    XPath uses "path like" syntax to identify and navigate nodes in a website's HTML (or more generally in any XML document).
    For more info refer to https://www.w3schools.com/xml/xpath_intro.asp
    """
    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, value=xpath)
        except NoSuchElementException:
            return False
        return True
    

class ScraperReuters(SeleniumScraper):
    """
    Scrape news articles from Reuters
    """
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

class ScraperMarketWatch(SeleniumScraper):
    """
    Scrape news articles from MarketWatch
    """
    def _getBody(self):
        total_text = ""
        xpath = f'//div[@id="js-article__body"]/descendant::p'
        if self.check_exists_by_xpath(xpath):
            marketwatch_paras = self.driver.find_elements(By.XPATH, value=xpath)
            for marketwatch_para in marketwatch_paras:
                total_text += marketwatch_para.text + "\n"
            
        self.article_body = total_text
