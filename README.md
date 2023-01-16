# SimpliFeed Backend

### NOTE: As the backend is hosted using Render free tier, it will go in sleep mode after 15 minutes if inactive, which will take about 20-30 seconds to wake up. Please ignore initial loading time.

Install libraries:
```
pip install -r requirements.txt
```

To run summarization model and scrape news articles
```
py scrape_yahoo_articles.py
```

To run backend app:
```
uvicorn main:app --reload
```


### Possible Difficulties:
- Selenium not working
  - Check your Chrome version and update chromedriver.exe accordingly from https://chromedriver.chromium.org/downloads
