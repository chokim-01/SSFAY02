from selenium import webdriver
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


modelpath = '/home/ubuntu/Model/'

# Load Model using pickle
with open(modelpath+'news_model.clf', 'rb') as models:
    news_model = pickle.load(models)

with open(modelpath+'local_model.clf', 'rb') as models:
    local_model = pickle.load(models)

with open(modelpath+'word_indices.clf', 'rb') as models:
    word_indices = pickle.load(models)


# get news contents, comments
def get_news(news_link_list):

    print("[+] Get news start")

    # data array
    news_save = []
    comment_save = []

    emoji = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

    for news_idx in range(len(news_link_list)):
        news_item = []

        print("[+] News_idx : ", (news_idx+1), "  Start")
        # Find oid, aid
        oid_idx = news_link_list[news_idx].find("oid=") + 4
        aid_idx = news_link_list[news_idx].find("&aid=")
        oid = news_link_list[news_idx][oid_idx:aid_idx]
        aid = news_link_list[news_idx][aid_idx + 5:]

        # Get news title, date, news_time
        req = requests.get(news_link_list[news_idx])
        news_html = req.text
        soup = bs4.BeautifulSoup(news_html, 'html.parser')
        title = soup.find('title').get_text()
        news_time = soup.find(class_='info').find('span').text
        
        if '기사입력' not in news_time:
            continue
        else:
            news_time = news_time[5:]
        
        date = re.sub('[.]','',news_time)[:8]

        # Parse content, Delete html tag
        content = (re.sub('<.+?>', '', str(soup.find(class_='news_end')), 0).strip())

        # Replace . -> \n, ." -> ."\n
        content = content.replace('."', '."\n')
        content = content.replace('. ', '.\n')

        # Save news content
        news_item.append(aid)
        news_item.append(title)
        news_item.append(content)
        news_item.append(date)
        news_item.append(news_time)
        news_save.append(news_item)
        
        # Control comments page
        comments_page_count = 0

        # Get news comments
        while True:
            comments_page_count += 1

            # Send header type
            header = {
                'Content-Type': 'application/json; charset=utf-8',
                "referer": news_link_list[news_idx]
            }
            # Send params type
            param = {'ticket': 'sports',
                     'pool': 'cbox2',
                     '_callback': 'jQuery21408666563295758771_1571805675151',
                     'templateId': 'view',
                     'lang': 'ko',
                     'objectId': 'news' + oid + ',' + aid,
                     'pageSize': '20',
                     'indexSize': '10',
                     'listType': 'OBJECT',
                     'pageType': 'more',
                     'page': comments_page_count,
                     }

            # Send url
            jquery_url = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json"

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
                comment_context = json_data["result"]["commentList"][idx]["contents"]
                
                # Del comments emoji
                comment_del_emoji = emoji.sub(r'', comment_context)
                
                comment_item.append(comment_del_emoji)
                reg_time = json_data["result"]["commentList"][idx]["regTime"]
                reg_time = reg_time[0: -5]
                comment_item.append(reg_time)
                comment_save.append(comment_item)
            
            time.sleep(0.1)
        
    return news_save, comment_save


def get_news_links(current_time):
    
    # Set date
    current_date = current_time.strftime('%Y%m%d')
    
    # Parse link & root url
    root_url = 'https://sports.news.naver.com'
    url = 'https://sports.news.naver.com/ranking/index.nhn?date='+current_date

    # popular news
    popular_news = deque()
    
    # Get request Use chromium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path='/home/ubuntu/Crontab/chromedriver', chrome_options=chrome_options)
    
    # Execute driver
    driver.implicitly_wait(3)
    driver.get(url)
    
    html_info = driver.page_source
   
    # Exit driver
    driver.quit()

    # Execute bs4, htmlparser, find link
    soup = bs4.BeautifulSoup(html_info, 'html.parser')
    content = [item for item in soup.find_all('a', class_='thmb') if len(item['class']) == 1]
   
    # Parse href
    for i in range(len(content)):
        popular_news.append(root_url + content[i].attrs['href'])

    return popular_news


# Load data
def load_data(news_link_list):
    # Get news data, comment data
    news_data, comments_data = get_news(news_link_list)

    comments_len = len(comments_data)

    # Comment data formmatting
    for cmt_idx in range(comments_len):
        comments_data[cmt_idx].append(int(0))
        comments_data[cmt_idx].append(int(0))
        comments_data[cmt_idx][0] = int(comments_data[cmt_idx][0])

    return news_data, comments_data


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
    sql = "insert into news (news_num, news_title, news_context, news_date, news_time) values(%s, %s, %s, %s, %s)"
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
def make_news_tag(news_data):
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

            word_list = []
            if len(word[0]) >= 2:
                word_list.append(word[0])
                word_list.append(word[1])
                word_list.append(int(news_data[news_idx][0]))
                tag.append(word_list)
                tag_cnt += 1

    return tag


# Make Tag with news_context
def make_comments_tag(comments_data):
    okt = Okt()
    tag = []

    # Append end point ( for add )
    comments_data.append([4, "End point"])

    comments_len = len(comments_data)
    word_count = Counter()
    news_num = comments_data[0][0]

    for comment_idx in range(comments_len):
        # get nouns from context

        if news_num != comments_data[comment_idx][0]:
            # sort by numbers
            sorted_word_count = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

            tag_cnt = 0
            for word in sorted_word_count:
                if tag_cnt > 100:
                    break
                word_list = []
                if len(word[0]) >= 2:
                    word_list.append(word[0])
                    word_list.append(word[1])
                    word_list.append(news_num)
                    tag.append(word_list)
                    tag_cnt += 1

            word_count = Counter()
            news_num = comments_data[comment_idx][0]

        else:
            context_nonce = okt.nouns(comments_data[comment_idx][1])
            word_count += Counter(context_nonce)

    return tag


# Add news
def add_to_db(news_data, comments_data, news_tag_data, comments_tag_data):
    if len(news_data) != 0:
        add_news(news_data)
        add_comments(comments_data)
        add_news_tag(news_tag_data)
        add_comments_tag(comments_tag_data)

    return


# Add comment to DB
def add_comments(comments_data):
    comments_data = comments_data[:-1]

    for comment in comments_data:
        label_news, label_local = load_mention(comment[1])
        comment[3] = label_news
        comment[4] = label_local

    db = conn.db()
    cursor = db.cursor()
    sql = "insert into comments(news_num, comment_context, comment_time," \
          " label_news, label_local) values (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, comments_data)

    db.commit()

    return


# Add news tag to DB
def add_news_tag(tag_data):
    db = conn.db()
    cursor = db.cursor()
    sql = "insert into newstag (newstag_name, newstag_count, news_num) values(%s, %s, %s)"
    cursor.executemany(sql, tag_data)
    db.commit()

    return


# Add comments tag to DB
def add_comments_tag(tag_data):
    db = conn.db()
    cursor = db.cursor()
    sql = "insert into commentstag (commentstag_name, commentstag_count, news_num) values(%s, %s, %s)"
    cursor.executemany(sql, tag_data)
    db.commit()

    return


def main():
    for idx in range(1,2):
        current_time = datetime.datetime.now()
        news_link_list = get_news_links(current_time - datetime.timedelta(days=idx))
        data = load_data(news_link_list)
        
        # Deduplicate before news
        news_data, comments_data = check_news_duplicate(data)
        
        # Make tag news, comments
        news_tag_data = make_news_tag(news_data)
        comments_tag_data = make_comments_tag(comments_data)

        # Insert into db , news, comments, tags
        add_to_db(news_data, comments_data, news_tag_data, comments_tag_data)
        print(str(current_time), " day complete")


if __name__ == '__main__':
    main()

