import pymysql


def db():
    return pymysql.connect(host='13.125.20.58', user='mac_ai', password='mac_ai!@', db='ssafynews_ai', charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)


def cursor():
    return db.cursor()
