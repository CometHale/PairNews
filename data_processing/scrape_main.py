import math
import data_processing.web as web
from data_processing.scrape_article import scrape, ScrapeData


PAGE_SIZE = 100
PAGE_LIMIT = 1

# Read News API key
with open("newsapikey.txt", "r") as apiFile:
    API_KEY = apiFile.read()


businessSourcesUrl = 'https://newsapi.org/v2/sources?country=us&language=en&category=business&apiKey={}'.format(API_KEY)
generalSourcesUrl = 'https://newsapi.org/v2/sources?country=us&language=en&category=general&apiKey={}'.format(API_KEY)

businessSourcesJson = web.get(businessSourcesUrl, shouldCache=False).json()
generalSourcesJson = web.get(generalSourcesUrl, shouldCache=False).json()

businessIds = [source["id"] for source in businessSourcesJson["sources"]]
generalIds = [source["id"] for source in generalSourcesJson["sources"]]

allIds = businessIds + generalIds
allIds.remove("google-news")

numBatches = int(math.ceil(len(allIds) / 20))

allArticleJsons = []

for batch in range(numBatches):
    ids = allIds[(batch*20):((batch+1)*20)]
    ids_csv = ",".join(ids)
    everythingUrl = 'https://newsapi.org/v2/everything?language=en&pageSize={}&page={}&sources={}&sortBy=publishedAt&apiKey={}'.format(
        PAGE_SIZE,
        1,
        ids_csv,
        API_KEY)
    response = web.get(everythingUrl, shouldCache=False).json()
    totalResults = response["totalResults"]
    numPages = int(math.ceil(totalResults / PAGE_SIZE))
    if PAGE_LIMIT != -1:
        numPages = min(numPages, PAGE_LIMIT)

    allArticleJsons += response["articles"]

    for page in range(2, numPages+1):
        print("Downloading page {} / {}".format(page, numPages))
        everythingUrl = 'https://newsapi.org/v2/everything?language=en&pageSize={}&page={}&sources={}&sortBy=publishedAt&apiKey={}'.format(
            PAGE_SIZE,
            page,
            ids_csv,
            API_KEY)
        response = web.get(everythingUrl, shouldCache=False).json()
        allArticleJsons += response["articles"]

# print(len(allArticleJsons))


numArticles = len(allArticleJsons)
allScrapedData = []
for articleNum in range(numArticles):
    articleJson = allArticleJsons[articleNum]
    scrapedData = scrape(articleJson)
    allScrapedData.append(scrapedData)
    print("Scraped article {} / {}".format(articleNum, numArticles))

# print(allScrapedData)
