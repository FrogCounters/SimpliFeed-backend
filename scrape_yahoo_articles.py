from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import requests
from connect_db import *
from scrape_article_template import *

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = AutoTokenizer.from_pretrained("maze508/fin-pegasus-tte")

model = AutoModelForSeq2SeqLM.from_pretrained(
    "maze508/fin-pegasus-tte").to(torch_device)

def model_inference(train_text, model, tokenizer, torch_device):
    """
    Summarise based on different word length
    """
    batch = tokenizer.prepare_seq2seq_batch(
        src_texts=train_text, return_tensors="pt").to(torch_device)

    gen = model.generate(**batch)
    res0 = tokenizer.batch_decode(gen, skip_special_tokens=True)[0]

    gen = model.generate(**batch, min_length=30, max_length=30)
    res1 = tokenizer.batch_decode(gen, skip_special_tokens=True)[0]

    gen = model.generate(**batch, min_length=50, max_length=50)
    res2 = tokenizer.batch_decode(gen, skip_special_tokens=True)[0]

    gen = model.generate(**batch, min_length=100, max_length=100)
    res3 = tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
    
    return [res0, res1, res2, res3]


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

        image_url = doc.find("div", {"class": "caas-img-container"})
        if image_url:
            img = image_url.find("img")
            if "src" in img:
                image_url = img["src"]
            else:
                image_url = ""
        else:
            image_url = ""

        title = doc.find(
            "div", {"class": "caas-title-wrapper"}).find("h1").text
        date = doc.find("time").text

        total_text = ""
        p = doc.find("div", {"class": "caas-body"}).find_all("p")
        for i in p:
            if i.text not in ["(Add details)", "Most Read from Bloomberg", "Most Read from Bloomberg Businessweek"]:
                total_text += i.text + "\n\n"

        # x = requests.post("https://0luimbkplf.execute-api.ap-southeast-1.amazonaws.com/initial/pred/", json={"inputs": total_text})
        # print(x)
        res = model_inference([total_text], model, tokenizer, torch_device)
        print(res[0])

        try:
            db.execute("INSERT INTO articles (title, actual_content, summary, category, published_date, image_url, url) VALUES (%s, %s, %s, %s, %s, %s, %s)", (
                title, total_text, f'{{"{res[0]}","{res[1]}","{res[2]}","{res[3]}"}}', key, date, image_url, url))
        except:
            print("ERROR")
        print()
