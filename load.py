from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime
import os
import logging


logging.basicConfig(filename="load.log", level=logging.INFO)

def getInfoFromSite(url = "https://news.ycombinator.com/"):
    """
    Функция возвращает список кортежей формата ("Новость","URL")
    :param url: Адрес сайта - по умолчанию https://news.ycombinator.com/
    :return:
    """
    try:
        data = requests.get(url).content
        parseData = BeautifulSoup(data,features="lxml")
        news = parseData.find_all("a","storylink")
        logging.info("Load data from cite finished successful")
        return [(post['href'], post.contents[0]) for post in news]
    except Exception as e:
        logging.error(str(e))

def generateDB(dbname = "news.db"):
    """
    Функция проверяет наличие базы данных и при её отсутствии создаёт
    :param dbname:
    :return:
    """
    if dbname not in os.listdir():
        logging.info("Creating new database")
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        cur.execute("""CREATE TABLE news (
        id      INTEGER   PRIMARY KEY AUTOINCREMENT
                          NOT NULL,
        title   TEXT      NOT NULL,
        url     TEXT      NOT NULL,
        created TIMESTAMP NOT NULL
    );
    
    """)
        con.commit()
        con.close()


def updateDB(elems,dbname = "news.db"):
    """
    Функция помещает элементы в базу данных, очищая БД. Что бы хранилось всего 30 записей.
    :param elems - список кортежей формата ("Новость","URL"):
    :param dbname:
    :return:
    """
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute("DELETE FROM news")
    for data in elems:
        cur.execute("INSERT INTO news(url,title,created) VALUES (?,?,?)",(*data,datetime.datetime.now()))
        con.commit()

def loadData():
    """
    Функция обновляет базу данных
    :return:
    """
    logging.info("DB updated")
    updateDB(getInfoFromSite())