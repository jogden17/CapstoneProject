import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# takes care of mac error when trying to use urlopen function -> stackoverflow
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

# ability to output multiple url on trending articles from google news
base = "https://www.google.com/"
link = "https://www.google.com/search?client=firefox-b-1-d&sca_esv=c48753f2ce9d3764&q=trending+news&tbm=nws&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWZJPk1C9buWu--tLPKEpSxLqGfZiWMqdk6VF37sVUbkfuZLTj2oNC7EnrW0kOrs5_OmipJdVTNqNxrP1hxJXbQxxTb_d6aiw0C9XShVsYl4bwwePt7xYHPiWHUhekC1Vs59H8OvAtrXIeRgVkoH9nFw-4hrhdMd8GWyIOMQnw_ZoqQa0OFUnE7PgaIjsyQBUlcE5T8A&sa=X&ved=2ahUKEwi5ufGCuNKGAxXTEmIAHX7jDc0Q0pQJegQICxAB&biw=1526&bih=870&dpr=2"
req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
with requests.Session() as c:
    b_soup = BeautifulSoup(webpage, "html5lib")
    for div_class in b_soup.find_all('div', attrs={'class': 'Gx5Zad fP1Qef xpd EtOod pkphOe'}):
        pre_split_link = div_class.find('a', href = True)['href']
        # final version of isolated links printed
        actual_link = (pre_split_link.split("/url?q=")[1]).split("&sa=U&")[0]

# example 1 from one of the trending links above, attempting to output article body
practice_link = "https://www.cgsentinel.com/news/trending-organizers-launch-spirit-of-bmd-celebration/article_ae870f72-2415-11ef-a8cc-8fd51abebf03.html"
req1 = Request(practice_link, headers={'User-Agent': 'Mozilla/5.0'})
webpage1 = urlopen(req1).read()
with requests.Session() as c:
    b_soup1 = BeautifulSoup(webpage1, "html5lib")
    for div_class in b_soup1.find_all('div', attrs={'class': 'subscriber-only'}):
        print(div_class)

print("NEXT PASSAGE")

# example 2 from one of the trending links above, attempting to output article body
practice_link = "https://www.wgauradio.com/news/trending/customs-officers-seize-159k-unreported-us-currency-200-rounds-ammo-border/V465DXMMWZHDRII7UYIIO25NEQ/"
req1 = Request(practice_link, headers={'User-Agent': 'Mozilla/5.0'})
webpage1 = urlopen(req1).read()
with requests.Session() as c:
    b_soup1 = BeautifulSoup(webpage1, "html5lib")
    for p_class in b_soup1.find_all('p', attrs={'class': 'default__StyledText-tl066j-0 gyoiDU body-paragraph'}):
        print(p_class)





