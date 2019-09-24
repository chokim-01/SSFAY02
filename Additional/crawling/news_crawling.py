from scipy.sparse import lil_matrix
from collections import deque
from konlpy.tag import Okt
import conn.conn as conn
import numpy as np
import datetime
import requests
import pickle
import json
import time
import bs4
import re

# Load Model using pickle
with open('../Model/news_model.clf', 'rb') as models:
   news_model = pickle.load(models)
with open('../Model/local_model.clf', 'rb') as models:
   local_model = pickle.load(models)
with open('../Model/word_indices.clf', 'rb') as models:
   word_indices = pickle.load(models)


def get_news(news_link_list):
    news_save = []
    comment_save = []

    news_cnt = 0
    for news_link in range(len(news_link_list)):
        news_item = []

        # Find oid, aid, date
        oid_idx = news_link_list[news_link].find("oid=") + 4
        aid_idx = news_link_list[news_link].find("&aid=")
        date_idx = news_link_list[news_link].find("&date")
        oid = news_link_list[news_link][oid_idx:aid_idx]
        aid = news_link_list[news_link][aid_idx+5:date_idx]
        date = news_link_list[news_link][date_idx+6:date_idx+14]

        # Get news title, content
        req = requests.get(news_link_list[news_link])
        news_html = req.text
        soup = bs4.BeautifulSoup(news_html, 'html.parser')
        title = soup.find('title').get_text()

        # Delete script tag
        for s in soup('script'):
            s.extract()

        # Delete html tag
        content = (re.sub('<.+?>', '', str(soup.find(class_='_article_body_contents')), 0).strip())

        # Replace . -> \n, ." -> ."\n
        content = content.replace('."', '."\n')
        content = content.replace('. ', '.\n')

        news_item.append(aid)
        news_item.append(title)
        news_item.append(content)
        news_item.append(date)
        news_save.append(news_item)

        # Control news page
        news_page_count = 0

        while True:
            news_page_count += 1

            # Send header type
            header = {
                'Content-Type': 'application/json; charset=utf-8',
                "referer": news_link_list[news_link]
            }

            # Send params type
            param = {'ticket': 'news',
                     'pool': 'cbox5',
                     '_callback': 'jQuery1707138182064460843_1523512042464',
                     'lang': 'ko',
                     'objectId': 'news' + oid + ',' + aid,
                     'pageSize': '20',
                     'indexSize': '10',
                     'listType': 'OBJECT',
                     'pageType': 'more',
                     'page': news_page_count
                     }

            jquery_url = "https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json"

            # Get request
            comment = requests.get(jquery_url, headers=header, params=param)

            # Find comment, str to json
            temp = comment.text
            json_start = temp.find('(')
            json_end = len(temp) - 2

            string_data = temp[json_start + 1:json_end]
            json_data = json.loads(string_data)

            comment_len = len(json_data["result"]["commentList"])
            if comment_len <= 1:
                break

            # Parse comment
            for idx in range(0, comment_len):
                comment_item = []
                if json_data["result"]["commentList"][idx]["contents"] is None:
                    break

                comment_item.append(aid)
                comment_item.append(json_data["result"]["commentList"][idx]["contents"])
                regtime = json_data["result"]["commentList"][idx]["regTime"]
                regtime = regtime[0: -5]

                comment_item.append(regtime)

                comment_save.append(comment_item)
            time.sleep(0.1)

        # Save news_data.clf, comment_data.clf
        # pickle.dump(news_save, open('news_data2.clf', 'wb'))
        # pickle.dump(comment_save, open('comment_data2.clf', 'wb'))

        news_cnt += 1
        print(news_save)
        print(comment_save)
    return news_save, comment_save


def get_news_links(current_time):
    # Parse link & root url
    root_url = 'https://news.naver.com'
    url = 'https://news.naver.com/main/ranking/popularDay.nhn'

    # 30 Days popular news
    popular_news = deque()

    # Set date
    current_date = current_time.strftime('%Y%m%d')

    # Send params type
    params = {'rankingType': 'popular_day',
              'sectionId': '100',
              'date': current_date
            }
    # Get request
    req = requests.get(url, params=params)

    # Execute bs4, htmlparser, find link
    soup = bs4.BeautifulSoup(req.content, 'html.parser')
    content = soup.find_all('a', class_='nclicks(rnk.gov)')

    for i in range(len(content)):
        if i % 2:
            continue
        popular_news.append(root_url+content[i].attrs['href'])

    return popular_news


# Load data
def load_data(news_link_list):
    # Get news data, comment data
    news_data, comments_data = get_news(news_link_list)
    news_len = len(news_data)
    news_d = [[_ for _ in range(4)] for _ in range(news_len)]

    # Count of Deduplication
    input_count = 0
    blank_count = 0

    for news_idx in range(news_len):
        flag = False

        # Skip duplicate news
        for news_before in range(news_idx):
            if news_data[news_idx][0] == news_d[news_before][0]:
                flag = True
                blank_count += 1
                break

        if flag:
            continue

        news_d[input_count] = news_data[news_idx]
        input_count += 1

    news_d = news_d[:input_count]

    comments_len = len(comments_data)

    # Comment data formmatting
    for cmt_idx in range(comments_len):
        comments_data[cmt_idx].append(int(0))
        comments_data[cmt_idx].append(int(0))
        comments_data[cmt_idx][0] = int(comments_data[cmt_idx][0])

    return news_d, comments_data


def tokenize_mention(data_row):
   """
   :param data_row:
   :return: tokenize data ([word/morpheme, word/morpheme, word/morpheme, ...]
   """
   okt = Okt()
   return ['/'.join(t) for t in okt.pos(data_row, norm=True, stem=True)]


# Add News test case to DB
def add_news(news_data):
    db = conn.db_hr()
    cursor = db.cursor()

    sql = "insert into news (news_num, news_title, news_context, news_date) values(%s, %s, %s, %s)"
    cursor.executemany(sql, news_data)
    db.commit()

    return ""


def load_mention(mention):
    """
    :param mention: sentence
    :return: negative 0, positive 1
    """
    # tokenize_mention of mention(sentence)
    mention_token_data = tokenize_mention(mention)
    # sparse matrix of mention(sentence)
    x_mention = lil_matrix((1, len(word_indices)), dtype=np.int64)
    # set sparse matirx of mention
    for token in mention_token_data:
        word = token.split("/")[0]
        if word in word_indices:
            x_mention[0, word_indices[word]] = 1
    return int(news_model.predict(x_mention)[0]), int(local_model.predict(x_mention)[0])


# Add comment case to DB
def add_comment(comments_data):

    for comment in comments_data:
        label_news, label_local = load_mention(comment[1])
        comment[2] = label_news
        comment[3] = label_local

    db = conn.db_hr()
    cursor = db.cursor()

    sql = "insert into comments(news_num, comment_context, comment_time," \
          " label_news, label_local) values (%s, %s, %s, %s, %s)"

    cursor.executemany(sql, comments_data)
    db.commit()

    return


def add_tag(tag_data):
    db = conn.db_hr()
    cursor = db.cursor()

    sql = "insert into tag (tag_name, news_num) values(%s, %s)"
    cursor.executemany(sql, tag_data)
    db.commit()

    return


# check table news duplicate
def check_news_duplicate(data):
    db = conn.db_hr()
    cursor = db.cursor()

    news_data, comments_data = data

    news_data_delete = []
    comments_data_delete = []
    for news in news_data:
        sql = "select count(*) as count from news where news_num = %s"
        cursor.execute(sql, news[0])

        rows = cursor.fetchall()

        if rows[0]['count'] == 0:
            news_data_delete.append(news)
            for comment in comments_data:
                if news[0][len(news[0]) - len(str(comment[0])):] == str(comment[0]):
                    comments_data_delete.append(comment)

    return news_data_delete, comments_data_delete


def add_testcase(data):
    news_data, comments_data = data

    news_len = len(news_data)
    tag = []

    for news_idx in range(news_len):
        title_nonce = tokenize_mention(news_data[news_idx][1])

        for title in title_nonce:
            title_class_list = []
            title_class = title.split("/")
            if title_class[1] == "Noun":
                title_class_list.append(title_class[0])
                title_class_list.append(int(news_data[news_idx][0]))
                tag.append(title_class_list)

    add_news(news_data)
    add_comment(comments_data)
    add_tag(tag)

    return


def main():
    current_time = datetime.datetime.now()

    for i in range(1, 8):
        start = time.time()
        news_link_list = get_news_links(current_time - datetime.timedelta(days=i))
        data = load_data(news_link_list)
        add_testcase(check_news_duplicate(data))
        print(" Endpoint : ", time.time() - start)


if __name__ == '__main__':
    main()
