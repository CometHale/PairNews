import requests

__cache = {}

def get(url, shouldCache=True):
    if shouldCache:
        if url in __cache:
            print("Hit: {}", url)
            return __cache[url]

    response = requests.get(url)
    print("Fetch: {}".format(url))
    if shouldCache:
        __cache[url] = response

    return response