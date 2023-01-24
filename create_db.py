from connect_db import *


def create_db_script():
    db.execute("CREATE TABLE IF NOT EXISTS articles ("
               "news_id SERIAL primary key, "
               "title VARCHAR, "
               "actual_content VARCHAR, "
               "summary text[], "
               "category VARCHAR(50), "
               "published_date TIMESTAMP, "
               "image_url VARCHAR(250), "
               "url VARCHAR(250) "
               ")")

    print("Database successfully updated/created...")


if __name__ == '__main__':
    create_db_script()
