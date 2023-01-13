from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

import time
# from connect_db import *
from scrape_finviz_article import ScraperBloomberg, ScraperReuters


def get_driver(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--enable-javascript")
    # chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--start-maximized')
    # chrome_options.add_argument('--start-fullscreen')
    # chrome_options.add_argument('--single-process') 
    serv = Service(os.getcwd()+'/chromedriver')
    driver = webdriver.Chrome(options=chrome_options, service=serv) 
    driver.get(url)
    return driver


endpoints = {"News": "news.ashx?v=2"}
publishers = {
    # "Bloomberg": ScraperBloomberg,
    "Reuters": ScraperReuters}
for key, endpoint in endpoints.items():
    driver = get_driver('https://finviz.com/news.ashx?v=2')
    finviz_publishers = driver.find_elements(By.XPATH, value='//a[@class="nn-title-link"]')

    for finviz_publisher in finviz_publishers:
        publisher_name = finviz_publisher.text
        if publisher_name in publishers:
            publisher_dirpath = os.path.join(os.getcwd(), "Publishers", publisher_name)

            if not os.path.exists(publisher_dirpath):
                os.makedirs(publisher_dirpath)
            
            
            
            finviz_articles = finviz_publisher.find_elements(By.XPATH, value='./../../../../../../following-sibling::tr[@class="nn"]')

            for finviz_article in finviz_articles:
                finviz_article_link = finviz_article.find_element(By.XPATH, value='./descendant::a')
                finviz_article_date = finviz_article.find_element(By.XPATH, value='./descendant::td[@class="nn-date"]')
                
                article_title = finviz_article_link.text
                article_date = finviz_article_date.text
                article_link = finviz_article_link.get_attribute('href')
                article_filename = article_date + "_" + article_title + ".txt"
                article_filepath = os.path.join(publisher_dirpath, article_filename)

                print("Loading link: " + article_link)
                article_scraper = publishers[publisher_name](url=article_link, title=article_title, date=article_date)

                with open(article_filepath, "w" ) as f:
                    f.write(article_scraper.getBody())

                del(article_scraper)

    # while True:
    #     x = driver.find_elements(By.XPATH, value='//*[@id="Fin-Stream"]/ul/li')
    #     time.sleep(5)
    #     if len(x) == last or len(x) >= 30:
    #         break
    #     else:
    #         last = len(x)
    #     driver.execute_script("window.scrollTo(0, 1000)")

    # for i in x:
    #     url = i.find_element(By.TAG_NAME, value="a").get_attribute('href')
    #     doc = get_page(url)
    #     print(url)

    #     if "/video/" in url:
    #         continue

    #     title = doc.find(
    #         "div", {"class": "caas-title-wrapper"}).find("h1").text
    #     date = doc.find("time").text

    #     total_text = ""
    #     p = doc.find("div", {"class": "caas-body"}).find_all("p")
    #     for i in p:
    #         total_text += i.text + "\n"
    #     print(total_text)

    #     #########################
    #     ### SUMMARISE HERE ######
    #     #########################

    #     print()

    #     # db.execute("INSERT INTO articles VALUES (%s, %s, %s, %s, %s, %s)", (
    #     #     title, total_text, "summary to be filled here", key, date, url))
