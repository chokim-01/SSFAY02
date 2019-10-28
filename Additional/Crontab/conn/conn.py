import pymysql


def db():
    return pymysql.connect(host='127.0.0.1', user='mac_ai', password='mac_ai!@', db='ssafynews_ai', charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)


def cursor():
    return db.cursor()
