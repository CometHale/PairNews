from bs4 import BeautifulSoup
import data_processing.web as web


def __largest_text(results):
    bestLen = 0
    bestText = ""
    for result in results:
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


SCRAPE_PATTERNS = {
    "fortune" : {
        "tagName" : "div",
        "idName" : "article-body",
        "className" : True
    }
}

def _scrape_text(url, sourceId):
    # url = "http://fortune.com/2018/01/20/google-ceo-has-no-regrets-about-firing-author-of-anti-diversity-memo/"
    html = web.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    if sourceId in SCRAPE_PATTERNS:
        pattern = SCRAPE_PATTERNS[sourceId]

        m = __match_tag(soup, tagName=pattern["tagName"], idName=pattern["idName"], className=pattern["className"])
        return __largest_text(m)
    else:
        print("ERR: No scraper implemented for source-id = {}".format(sourceId))
        return html

class ScrapeData:
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
    return ScrapeData(textData=text,
                      title=articleJson["title"],
                      sourceId=sourceId,
                      sourceName=articleJson["source"]["name"],
                      url=url,
                      publishDate=articleJson["publishedAt"])
