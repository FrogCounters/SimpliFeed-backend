from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from connect_db import *
from scrape_article import *


def get_driver(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--start-fullscreen')
    chrome_options.add_argument('--single-process')
    serv = Service(os.getcwd()+'/chromedriver')
    driver = webdriver.Chrome(options=chrome_options, service=serv)
    driver.get(url)
    return driver


# endpoints = ["news", "topic/economic-news", "live/politics",
#              "topic/stock-market-news", "topic/crypto"]

endpoints = {"News": "news", "Economics": "topic/economic-news",
             "Politics": "live/politics", "Stocks": "topic/stock-market-news", "Crypto": "topic/crypto"}

for key, endpoint in endpoints.items():
    driver = get_driver(f'https://finance.yahoo.com/{endpoint}')

    last = 0
    while True:
        x = driver.find_elements(By.XPATH, value='//*[@id="Fin-Stream"]/ul/li')
        time.sleep(5)
        if len(x) == last or len(x) >= 30:
            break
        else:
            last = len(x)
        driver.execute_script("window.scrollTo(0, 1000)")

    for i in x:
        url = i.find_element(By.TAG_NAME, value="a").get_attribute('href')
        doc = get_page(url)
        print(url)

        if "/video/" in url:
            continue

        title = doc.find(
            "div", {"class": "caas-title-wrapper"}).find("h1").text
        date = doc.find("time").text

        total_text = ""
        p = doc.find("div", {"class": "caas-body"}).find_all("p")
        for i in p:
            total_text += i.text + "\n"
        print(total_text)

        #########################
        ### SUMMARISE HERE ######
        #########################

        print()

        db.execute("INSERT INTO articles VALUES (%s, %s, %s, %s, %s)", (
            title, total_text, key, date, url))
