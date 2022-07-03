import requests
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}


def makeRequest():
    for i in range(0, 9):
        RTrequest = requests.get("https://www.rt.com/search?q=Ukraine&type=", headers = headers)

        if RTrequest.status_code != 200:
            print("Bad Request")
        else:
            return RTrequest.text
        
RTtext = makeRequest()
#print(RTtext)
soup = BeautifulSoup(RTtext, "html.parser")

results = []

def parseHTML():
    newsItems = soup.select(".list-card")
    
    for item in newsItems:
        title = item.select_one(".list-card__content > .list-card__content--title.link_hover > .link.link_hover").text
        image = item.select_one(".card__cover > .media > .media__image > a > noscript > img")["src"]
        date = item.select_one(".list-card__content > .card__date > span.date").text
        
        article = {"title": title.strip(), "image" : image, "date" : date}
        print(title, image, date)
        results.append(article)
    
parseHTML()

#print (results)


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goormtest_web_apr.settings")
import django
django.setup()

from hello.models import Article

Article.objects.filter(source="RT").delete()

for result in results:
    Article.objects.create(title=result["title"], image=result["image"], date=result["date"], source="RT")
    

print(Article.objects.all())
