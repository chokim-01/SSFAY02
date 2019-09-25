from collections import deque, Counter
from scipy.sparse import lil_matrix
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


# get news contents, comments
def get_news(news_link_list):
    print("Get news...")
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
        aid = news_link_list[news_link][aid_idx + 5:date_idx]
        date = news_link_list[news_link][date_idx + 6:date_idx + 14]

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

        # Save news content
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

            # Send url
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

                # Save news comments
                comment_item.append(aid)
                comment_item.append(json_data["result"]["commentList"][idx]["contents"])
                reg_time = json_data["result"]["commentList"][idx]["regTime"]
                reg_time = reg_time[0: -5]
                comment_item.append(reg_time)
                comment_save.append(comment_item)
            time.sleep(0.1)
        news_cnt += 1
        print("news number : ", news_cnt)

    print("Get news complete")
    return news_save, comment_save


def get_news_links(current_time):
    print("time : ", current_time)

    # Parse link & root url
    root_url = 'https://news.naver.com'
    url = 'https://news.naver.com/main/ranking/popularDay.nhn'

    # 30 Days popular news
    popular_news = deque()

    # Set date
    current_date = current_time.strftime('%Y%m%d')

    # Send params type
    params = {
        'rankingType': 'popular_day', 'sectionId': '100', 'date': current_date
    }

    # Get request
    req = requests.get(url, params=params)

    # Execute bs4, htmlparser, find link
    soup = bs4.BeautifulSoup(req.content, 'html.parser')
    content = soup.find_all('a', class_='nclicks(rnk.gov)')

    for i in range(len(content)):
        if i % 2:
            continue
        popular_news.append(root_url + content[i].attrs['href'])

    return popular_news


# Load data
def load_data(news_link_list):
    # Get news data, comment data
    news_data, comments_data = get_news(news_link_list)
    news_len = len(news_data)

    print("load data...")
    news_data_reset = [[_ for _ in range(4)] for _ in range(news_len)]

    # Count of Deduplication
    input_idx = 0

    for news_idx in range(news_len):
        flag = False

        # Skip duplicate news
        for news_before in range(news_idx):
            if news_data[news_idx][0] == news_data_reset[news_before][0]:
                flag = True
                break

        if flag:
            continue

        news_data_reset[input_idx] = news_data[news_idx]
        input_idx += 1

    # Deleted duplicate news contents, comments list
    news_data_reset = news_data_reset[:input_idx]
    comments_len = len(comments_data)

    # Comment data formmatting
    for cmt_idx in range(comments_len):
        comments_data[cmt_idx].append(int(0))
        comments_data[cmt_idx].append(int(0))
        comments_data[cmt_idx][0] = int(comments_data[cmt_idx][0])

    print("load complete")
    return news_data_reset, comments_data


def tokenize_mention(data_row):
    """
    :param data_row:
    :return: tokenize data ([word/morpheme, word/morpheme, word/morpheme, ...]
    """
    okt = Okt()

    return ['/'.join(t) for t in okt.pos(data_row, norm=True, stem=True)]


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


# Add News to DB
def add_news(news_data):
    db = conn.db()
    cursor = db.cursor()
    sql = "insert into news (news_num, news_title, news_context, news_date) values(%s, %s, %s, %s)"
    cursor.executemany(sql, news_data)
    db.commit()

    return ""


# check DB table duplicate news
def check_news_duplicate(data):
    db = conn.db()
    cursor = db.cursor()
    news_data, comments_data = data

    # Delete duplicate in DB table
    news_data_delete = []
    comments_data_delete = []

    for news in news_data:
        sql = "select count(*) as count from news where news_num = %s"
        cursor.execute(sql, news[0])
        rows = cursor.fetchall()

        # if not duplicate
        if rows[0]['count'] == 0:
            news_data_delete.append(news)

            for comment in comments_data:
                if news[0][len(news[0]) - len(str(comment[0])):] == str(comment[0]):
                    comments_data_delete.append(comment)

    return news_data_delete, comments_data_delete


# Make Tag with news_context
def make_tag(news_data):
    news_len = len(news_data)
    okt = Okt()
    tag = []

    for news_idx in range(news_len):
        # get nouns from context
        context_nonce = okt.nouns(news_data[news_idx][2])
        word_count = Counter(context_nonce)

        # sort by numbers
        sorted_word_count = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

        tag_cnt = 0
        for word in sorted_word_count:
            if tag_cnt >= 5:
                break

            word_list = []
            if len(word[0]) >= 2:
                word_list.append(word[0])
                word_list.append(int(news_data[news_idx][0]))
                tag.append(word_list)
                tag_cnt += 1

    return tag


# Add news
def add_news(data):
    if len(data) != 0:
        print("Insert DB...")
        news_data, comments_data = data
        add_news(news_data)
        add_comment(comments_data)
        tag = make_tag(news_data)
        add_tag(tag)

    return


# Add comment to DB
def add_comment(comments_data):
    for comment in comments_data:
        label_news, label_local = load_mention(comment[1])
        comment[2] = label_news
        comment[3] = label_local

    db = conn.db()
    cursor = db.cursor()
    sql = "insert into comments(news_num, comment_context, comment_time," \
          " label_news, label_local) values (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, comments_data)

    db.commit()

    return


# Add tag to DB
def add_tag(tag_data):
    db = conn.db()
    cursor = db.cursor()
    sql = "insert into tag (tag_name, news_num) values(%s, %s)"
    cursor.executemany(sql, tag_data)
    db.commit()

    return


def main():
    current_time = datetime.datetime.now()
    news_link_list = get_news_links(current_time - datetime.timedelta(days=1))
    data = load_data(news_link_list)

    # Add yesterday news
    add_news(check_news_duplicate(data))
    print("complete")


if __name__ == '__main__':
    main()
