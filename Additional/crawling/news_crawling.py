import json
from collections import deque
import datetime
import requests
import bs4
import time
import re
import pickle


def get_news(news_link_list):
    comment = deque()
    news_save = deque()
    comment_save = deque()

    news_cnt = 0
    for news_link in range(len(news_link_list)):
        news_item = deque()

        # Find oid, aid, date, page
        oid_idx = news_link_list[news_link].find("oid=") + 4
        aid_idx = news_link_list[news_link].find("&aid=")
        date_idx = news_link_list[news_link].find("&date")
        oid = news_link_list[news_link][oid_idx:aid_idx]
        aid = news_link_list[news_link][aid_idx+5:date_idx]
        date = news_link_list[news_link][date_idx+6:date_idx+14]
        page = 0

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

        # Get news comment
        news_page_count = 0

        while news_page_count < 50:
            news_page_count += 1
            page += 1

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
                     'page': page
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
                comment_item = deque()
                if json_data["result"]["commentList"][idx]["contents"] is None:
                    break
                comment_item.append(aid)
                comment_item.append(json_data["result"]["commentList"][idx]["contents"])
                comment_save.append(comment_item)
            time.sleep(0.1)

        # Save news_data.clf, comment_data.clf
        pickle.dump(news_save, open('news_data.clf', 'wb'))
        pickle.dump(comment_save, open('comment_data.clf', 'wb'))
        news_cnt += 1
        print(news_cnt)


def get_news_links():
    # Parse link & root url
    root_url = 'https://news.naver.com'
    url = 'https://news.naver.com/main/ranking/popularDay.nhn'

    # 30 Days popular news
    popular_news = deque()

    for idx in range(1, 30):
        # Set date
        current_time = datetime.datetime.now() - datetime.timedelta(days=idx)
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


def main():
    news_link_list = get_news_links()
    get_news(news_link_list)


if __name__ == '__main__':
    main()
