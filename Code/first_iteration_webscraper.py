import requests
from bs4 import BeautifulSoup
import ssl

# function to retrieve trending news urls from gNews. *ONLY WORKS W/ GNEWS*
def get_trending_news_urls(link):
    response = requests.get(link)
    if response.status_code != 200:
        print("failure")
    b_soup = BeautifulSoup(response.content, "html5lib")
    links = []
    for div_class in b_soup.find_all('div', attrs={'class': 'Gx5Zad fP1Qef xpd EtOod pkphOe'}):
        pre_split_link = div_class.find('a', href=True)['href']
        actual_link = (pre_split_link.split("/url?q=")[1]).split("&sa=U&")[0]
        links.append(actual_link)
    return links

# function to retrieve the article body from a given url
def get_article_body(url, tag, class_name):
    response = requests.get(url)
    if response.status_code != 200:
        print("failure")
    b_soup = BeautifulSoup(response.content, "html5lib")
    for x in b_soup.find_all(tag, attrs={'class': class_name}):
        print(x.get_text())


# TESTING FUNCTIONS

# trending links
link = "https://www.google.com/search?client=firefox-b-1-d&sca_esv=c48753f2ce9d3764&q=trending+news&tbm=nws&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWZJPk1C9buWu--tLPKEpSxLqGfZiWMqdk6VF37sVUbkfuZLTj2oNC7EnrW0kOrs5_OmipJdVTNqNxrP1hxJXbQxxTb_d6aiw0C9XShVsYl4bwwePt7xYHPiWHUhekC1Vs59H8OvAtrXIeRgVkoH9nFw-4hrhdMd8GWyIOMQnw_ZoqQa0OFUnE7PgaIjsyQBUlcE5T8A&sa=X&ved=2ahUKEwi5ufGCuNKGAxXTEmIAHX7jDc0Q0pQJegQICxAB&biw=1526&bih=870&dpr=2"
trending_urls = get_trending_news_urls(link)
print(trending_urls)

print("---------------------PASSAGES---------------------")

# example 1: attempting to output article body
practice_link_1 = "https://www.cgsentinel.com/news/trending-organizers-launch-spirit-of-bmd-celebration/article_ae870f72-2415-11ef-a8cc-8fd51abebf03.html"
print("Article Body from first example:")
get_article_body(practice_link_1, 'div', 'subscriber-only')

print("---------------------NEXT PASSAGE---------------------")

# example 2: attempting to output article body
practice_link_2 = "https://www.wgauradio.com/news/trending/customs-officers-seize-159k-unreported-us-currency-200-rounds-ammo-border/V465DXMMWZHDRII7UYIIO25NEQ/"
print("Article Body from second example:")
get_article_body(practice_link_2, 'p', 'default__StyledText-tl066j-0 gyoiDU body-paragraph')
