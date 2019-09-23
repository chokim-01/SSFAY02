import pymysql


def db():
    return pymysql.connect(host='localhost', user='root', password='toor', db='ssafynews_ai', charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)


def cursor():
    return db.cursor()