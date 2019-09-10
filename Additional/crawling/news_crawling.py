import json
from collections import deque
import datetime
import requests
import bs4
import time
import re


def get_news(news_link_list):
    for i in range(len(news_link_list)):
        print(news_link_list[i])
        a = news_link_list[i].find("oid=") + 4
        b = news_link_list[i].find("&aid=")
        c = news_link_list[i].find("&date")

        dat = deque()
        oid = news_link_list[i][a:b]
        aid = news_link_list[i][b + 5:c]
        page = 0

        # get title, content
        # req = requests.get(news_link_list)
        # news_html = req.text
        # soup = bs4.BeautifulSoup(news_html, 'html.parser')
        # title = soup.find('title').get_text()
        #
        # for s in soup('script'):
        #     s.extract()
        #
        # content = (re.sub('<.+?>', '', str(soup.find(class_='_article_body_contents')), 0).strip())
        #
        # content = content.replace('."', '."\n')
        # content = content.replace('. ', '.\n')
        #
        # comment = soup.find('li')
        #
        # print(title)
        # print(content)
        # print(comment)

        # get comment
        while True:
            page += 1
            header = {
                'Content-Type': 'application/json; charset=utf-8',
                "referer": news_link_list[i]
            }

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

            response_comment = requests.get(jquery_url, headers=header, params=param)
            time.sleep(1)

            temp = response_comment.text
            json_start = temp.find('(')
            json_end = len(temp) - 2

            string_data = temp[json_start + 1:json_end]

            json_data = json.loads(string_data)

            comment_len = len(json_data["result"]["commentList"])

            if comment_len <= 1:
                break

            for i in range(0, comment_len):
                if json_data["result"]["commentList"][i]["contents"] is None:
                    break

                dat.append(json_data["result"]["commentList"][i]["contents"])
                print(json_data["result"]["commentList"][i]["contents"])


def get_news_links():
    # Parse link & root url
    root_url = 'https://news.naver.com'
    url = 'https://news.naver.com/main/ranking/popularDay.nhn'

    # 30 Days popular news
    popular_news = deque()

    for idx in range(0, 30):
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
