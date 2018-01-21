import requests

__cache = {}

def get(url, shouldCache=True):
    if shouldCache:
        if url in __cache:
            print("Hit: {}", url)
            return __cache[url]

    try:
        response = requests.get(url)
        if response.status_code == 404:
            print("ERR: could not fetch url = {}".format(url))
            return None
    except Exception as err:
        print("ERR: could not fetch url = {}, err = {}".format(url, err))
        return None

    print("Fetch: {}".format(url))
    if shouldCache:
        __cache[url] = response

    return response