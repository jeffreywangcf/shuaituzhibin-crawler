# class URL:
#     def __init__(self, url, command):
#         self.url = url
#         self.command = command      #command can only be either "gathering" or "parsing"
#     def __eq__(self, other):
#         return self.url == other.url
#     def __ne__(self, other):
#         return self.url != other.url


class UrlManager:

    def __init__(self):
        self.archived_url = set()
        self.queue = set()

    def addNewUrl(self, urls):
        if urls is None:
            return
        if isinstance(urls, list) or isinstance(urls, tuple):
            urls = list(filter(lambda item: item != "javascript:;", urls))
            new_urls = set(urls) - (set(urls) & self.archived_url)
            self.queue = self.queue | new_urls
        else:
            if urls not in self.archived_url:
                if urls == "javascript:;":
                    return
                self.queue.add(urls)

    def isEmpty(self):
        return len(self.queue) == 0

    def getUrl(self):
        ret = self.queue.pop()
        self.archived_url.add(ret)
        return ret

    def getUrls(self):
        self.archived_url.update(self.queue)
        ret = list(self.queue)
        self.queue = set()
        return ret