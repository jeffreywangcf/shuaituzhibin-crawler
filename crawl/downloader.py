from bs4 import BeautifulSoup
from selenium import webdriver
from urllib import request

class Downloader:

    def __init__(self, start_url):
        self.start_url = start_url
        self.driver = None
        self.next_page_tag = None
        self.driver = webdriver.Chrome("/Users/Excited/chromedriver")  # replace tp your own ABSOLUTE path
        self.driver.get(self.start_url)

    def downloadPageSource(self):
        return self.driver.page_source

    def updatePageSource(self, via = "click"):
        assert isinstance(self.next_page_tag, str)
        if via == "click":
            try:
                self.driver.find_element_by_link_text(self.next_page_tag).click()
            except: return False
        return True

    def getPageSourceViaRequest(self, url):
        res = request.urlopen(url)
        if res.getcode() == 200:
            return res.read()
        return None