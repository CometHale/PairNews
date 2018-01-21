import math
import web as web
import json
import signal
import re
from scrape_article import scrape, ScrapeData

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.kill_now = True


PAGE_SIZE = 100
PAGE_LIMIT = 1

# Read News API key
with open("newsapikey.txt", "r") as apiFile:
    API_KEY = apiFile.read()

# Read scrape_store to see the currently imported articles
with open("scrape_store.json", "r") as storeFile:
    jsonStore = json.load(storeFile)
    store = [ScrapeData.fromJson(jsonDict) for jsonDict in jsonStore]
    urls = [data.url for data in store]
    urlSet = set(urls)

def filter_not_in_urls(articleJsons, urlSet):
    return [article for article in articleJsons if article["url"] not in urlSet]


urlBlacklist = [
    re.compile(r".*usatoday\.com/story/sports/.*"),
    re.compile(r".*ftw\.usatoday.*"),
    re.compile(r".*usatoday\.com/picture-gallery/.*"),
    re.compile(r".*/video/.*"),
    re.compile(r".*/videos/.*"),
    re.compile(r".*video\.foxnews\.com.*"),
    re.compile(r".*www\.wsj\.com.*"),
    re.compile(r".*overwatchwire\.usatoday\.com.*"),
    re.compile(r".*reuters\.com.*/soccer-portugal-standings/.*"),
    re.compile(r".*reuters\.com.*/.*-tennis-ausopen-.*/.*"),
    re.compile(r".*reuters\.com.*/us-olympics-2018-sno-.*/.*"),
    re.compile(r".*washingtonpost\.com/sports/.*"),
    re.compile(r".*washingtonpost\.com/news/capital-weather-gang/.*"),
    re.compile(r".*abcnews.*/Sports/.*"),
    re.compile(r".*reuters.*/sportsNews/.*"),
    re.compile(r".*reuters.*/us-mma-.*"),
    re.compile(r".*abc.*/shows/.*")
]

def matches_none(url, reList):
    for r in reList:
        if r.match(url) != None:
            return False
    return True

def filter_junk_urls(articleJsons):
    return [article for article in articleJsons if matches_none(article["url"], urlBlacklist)]


businessSourcesUrl = 'https://newsapi.org/v2/sources?country=us&language=en&category=business&apiKey={}'.format(API_KEY)
generalSourcesUrl = 'https://newsapi.org/v2/sources?country=us&language=en&category=general&apiKey={}'.format(API_KEY)

businessSourcesJson = web.get(businessSourcesUrl, shouldCache=False).json()
generalSourcesJson = web.get(generalSourcesUrl, shouldCache=False).json()

businessIds = [source["id"] for source in businessSourcesJson["sources"]]
generalIds = [source["id"] for source in generalSourcesJson["sources"]]

allIds = businessIds + generalIds
allIds.remove("google-news")
allIds.remove("reddit-r-all")


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

    allArticleJsons += filter_junk_urls(filter_not_in_urls(response["articles"], urlSet))

    for page in range(2, numPages+1):
        print("Downloading page {} / {}".format(page, numPages))
        everythingUrl = 'https://newsapi.org/v2/everything?language=en&pageSize={}&page={}&sources={}&sortBy=publishedAt&apiKey={}'.format(
            PAGE_SIZE,
            page,
            ids_csv,
            API_KEY)
        response = web.get(everythingUrl, shouldCache=False).json()
        allArticleJsons += filter_junk_urls(filter_not_in_urls(response["articles"], urlSet))

# print(len(allArticleJsons))


killer = GracefulKiller()
numArticles = len(allArticleJsons)

for articleNum in range(numArticles):
    articleJson = allArticleJsons[articleNum]

    try:
        scrapedData = scrape(articleJson)
    except Exception as err:
        print("ERR: Error scraping article = {}, error = {}".format(articleJson, err))
        scrapedData = None

    if scrapedData != None:
        jsonStore.append(scrapedData.toJson())

    print("Scraped article {} / {}".format(articleNum, numArticles))

    if killer.kill_now:
        break

with open("scrape_store.json", "w") as outputFile:
    print("Writing store back to JSON")
    json.dump(jsonStore, outputFile)

# print(allScrapedData)
