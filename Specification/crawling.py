from collections import deque
import datetime
import requests
import bs4
def get_newslinks():
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
    get_newslinks()
if __name__ == '__main__':
    main()
