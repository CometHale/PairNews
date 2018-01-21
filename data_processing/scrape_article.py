from bs4 import BeautifulSoup
import web


def __largest_text(results):
    if type(results) is str:
        return results

    bestLen = 0
    bestText = ""
    for result in results:
        if type(result) is str:
            text = result
        else:
            text = result.get_text()
        l = len(text)
        if l > bestLen:
            bestLen = l
            bestText = text
    return bestText

def __match_tag(soup, tagName, idName=True, className=True):
    return soup.find_all(tagName, attrs={
        "id": idName,
        "class": className
    })


def __scrape_fortune(soup):
    return __match_tag(soup, "div", idName="article-body", className=None)

def __scrape_the_hill(soup):
    mainMatches = __match_tag(soup, "div", idName=None, className="field-items")
    textMatches = map(lambda mainStoryTag: "\n".join([tag.get_text() for tag in mainStoryTag.find_all("p")]), mainMatches)
    return textMatches

def __scrape_politico(soup):
    mainStoryTag = __match_tag(soup, "div", idName=None, className="story-text")[0]
    return "\n".join([tag.get_text() for tag in mainStoryTag.find_all("p")])

def __scrape_breitbart(soup):
    mainMatches = __match_tag(soup, "div", idName=None, className="entry-content")
    textMatches = map(lambda mainStoryTag: "\n".join([tag.get_text() for tag in mainStoryTag.find_all("p")]), mainMatches)
    return textMatches


SCRAPE_FUNCS = {
    "fortune" : __scrape_fortune,
    "the-hill" : __scrape_the_hill,
    "politico" : __scrape_politico,
    "breitbart-news": __scrape_breitbart,
}

def _scrape_text(url, sourceId):
    # url = "http://fortune.com/2018/01/20/google-ceo-has-no-regrets-about-firing-author-of-anti-diversity-memo/"
    # sourceId = "fortune"
    res = web.get(url)
    if res == None:
        return None

    html = res.content
    soup = BeautifulSoup(html, 'html.parser')

    if sourceId in SCRAPE_FUNCS:
        func = SCRAPE_FUNCS[sourceId]
        text = __largest_text(func(soup))
        return text
    else:
        print("ERR: No scraper implemented for source-id = {}".format(sourceId))
        return None

class ScrapeData:
    def fromJson(jsonDict):
        return ScrapeData(jsonDict["textData"],
                          jsonDict["title"],
                          jsonDict["sourceId"],
                          jsonDict["sourceName"],
                          jsonDict["url"],
                          jsonDict["publishDate"])

    def toJson(self):
        return {
            "textData": self.textData,
            "title": self.title,
            "sourceId": self.sourceId,
            "sourceName": self.sourceName,
            "url": self.url,
            "publishDate": self.publishDate
        }

    def __init__(self, textData, title, sourceId, sourceName, url, publishDate):
        self.textData = textData
        self.title = title
        self.sourceName = sourceName
        self.sourceId = sourceId
        self.url = url
        self.publishDate = publishDate
    def __str__(self):
        return "title = {}, sourceName = {}, sourceId = {}, url = {}, publishDate = {}, textData = {}\n".format(
            self.title,
            self.sourceName,
            self.sourceId,
            self.url,
            self.publishDate,
            self.textData)
    __repr__ = __str__

def scrape(articleJson):
    sourceId = articleJson["source"]["id"]
    url = articleJson["url"]
    text = _scrape_text(url=url, sourceId=sourceId)
    if text == None:
        return None

    return ScrapeData(textData=text,
                      title=articleJson["title"],
                      sourceId=sourceId,
                      sourceName=articleJson["source"]["name"],
                      url=url,
                      publishDate=articleJson["publishedAt"])
