from connect_db import *


def create_db_script():
    db.execute("CREATE TABLE IF NOT EXISTS articles ("
               "title VARCHAR, "
               "actual_content VARCHAR, "
               "summary VARCHAR, "
               "category VARCHAR(50), "
               "published_date TIMESTAMP, "
               "url VARCHAR(250) "
               ")")

    print("Database successfully updated/created...")


if __name__ == '__main__':
    create_db_script()
