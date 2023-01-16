from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from scrape_finviz_article import ScraperReuters, ScraperMarketWatch


def get_driver(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    serv = Service(os.getcwd()+'/chromedriver')
    driver = webdriver.Chrome(options=chrome_options, service=serv) 
    driver.get(url)
    return driver


endpoints = {"News": "news.ashx?v=2"}
publishers = {
    "Reuters": ScraperReuters,
    "MarketWatch": ScraperMarketWatch,
    }
for key, endpoint in endpoints.items():
    driver = get_driver('https://finviz.com/news.ashx?v=2')
    finviz_publishers = driver.find_elements(By.XPATH, value='//a[@class="nn-title-link"]')
    articles = []
    for finviz_publisher in finviz_publishers:
        file_count =0 
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
            
                article_filename = publisher_name + f"-{file_count}" + ".json"
                file_count += 1
                article_filepath = os.path.join(publisher_dirpath, article_filename)
                articles.append((article_title, article_date, article_link, article_filename, article_filepath, publisher_name))

    for article in articles:
        article_title, article_date, article_link, article_filename, article_filepath, publisher_name = article
        print("Loading link: " + article_link)
        article_scraper = publishers[publisher_name](url=article_link, title=article_title, date=article_date)

        with open(article_filepath, "w" ) as f:
            article_json = {
                "title":article_title,
                "total_text":article_scraper.getBody(),
                "summary":"summary to be filled here",
                "key":"Finviz_" + publisher_name,
                "date":article_date,
                "url":article_link,
            }
            json.dump(article_json, f)
        
        article_scraper.driver.close()

        del(article_scraper)
