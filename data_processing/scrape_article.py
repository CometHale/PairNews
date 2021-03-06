from bs4 import BeautifulSoup
from newspaper import fulltext
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

def __remove_tag(soup, tagName, idName=True, className=True):
    badTags = __match_tag(soup, "div", idName=idName, className=className)
    for b in badTags:
        b.decompose()



def __scrape_fortune(soup):
    return __match_tag(soup, "div", idName="article-body", className=None)

def __scrape_the_hill(soup):
    __remove_tag(soup, "span", idName=True, className="rollover-people-block")

    mainMatches = __match_tag(soup, "div", idName=None, className="field-items")
    textMatches = map(lambda mainStoryTag: "\n".join([tag.get_text() for tag in mainStoryTag.find_all("p")]), mainMatches)
    return textMatches

def __scrape_politico(soup):
    __remove_tag(soup, "div", idName=None, className="story-supplement")

    mainStoryTag = __match_tag(soup, "div", idName=None, className="story-text")[0]
    return "\n".join([tag.get_text() for tag in mainStoryTag.find_all("p")])

def __scrape_breitbart(soup):
    mainMatches = __match_tag(soup, "div", idName=None, className="entry-content")
    textMatches = map(lambda mainStoryTag: "\n".join([tag.get_text() for tag in mainStoryTag.find_all("p")]), mainMatches)
    return textMatches

def __scrape_huffington_post(soup):
    matches = __match_tag(soup, "div", idName=None, className="entry__text")
    mainStoryTag = matches[0]
    return "\n".join([tag.get_text() for tag in __match_tag(mainStoryTag, "div", idName=None, className="content-list-component")])

def __scrape_new_york_time(soup):
    __remove_tag(soup, "div", idName="newsletter-promo", className=True)
    return __default_scrape(soup)

def __scrape_usa_today(soup):
    __remove_tag(soup, "span", idName=None, className="exclude-from-newsgate")
    text = __default_scrape(soup)
    return text.replace("Related Stories:", "")

def __scrape_abc(soup):
    mainStoryTag = __match_tag(soup, "div", idName=None, className="article-copy")[0]
    return "\n".join([tag.get_text() for tag in mainStoryTag.find_all("p", attrs={"itemprop" : "articleBody"})])

def __default_scrape(soup):
    try:
        return fulltext(str(soup))
    except Exception as err:
        print("ERR: could not parse HTML!")
        return None

SCRAPE_FUNCS = {
    "fortune" : __scrape_fortune,
    "the-hill" : __scrape_the_hill,
    "politico" : __scrape_politico,
    "breitbart-news" : __scrape_breitbart,
    "cnn" : __default_scrape,
    "the-huffington-post" : __scrape_huffington_post,
    "the-new-york-times" : __scrape_new_york_time,
    "usa-today" : __scrape_usa_today,
    "abc-news" : __scrape_abc,

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
        print("WARN: No scraper implemented for source-id = {}".format(sourceId))
        return __default_scrape(soup)

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
