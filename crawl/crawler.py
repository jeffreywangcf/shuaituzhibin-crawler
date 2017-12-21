from crawl import url_manager
from crawl import parser
from crawl import downloader
from crawl import outputer
import time
import random
import os
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor as tpe


class Crawler:

    def __init__(self, start_url, thread_pool_size = 5):
        self.count = int()
        self.thread_pool_size = thread_pool_size
        self.buffer_trigger = Event()
        self.url_manager = url_manager.UrlManager()
        self.parser = parser.Parser()
        self.downloader = downloader.Downloader(start_url)
        self.outputer = outputer.Outputer(self.buffer_trigger, "demo", "ShuaiTuZhiBin_Database")

    def startCrawl(self, toggle_print = True):

        def parse_new_urls():           #parse catalog page that returns urls of hero page
            while self.downloader.updatePageSource():
                raw_html = self.downloader.downloadPageSource()
                new_urls, next_page_tag = self.parser.parse(raw_html, self.downloader.start_url)
                self.url_manager.addNewUrl(new_urls)

        def parse_detail(in_url):        #parse hero pages
            if toggle_print:
                print("%d: gathering data from: %s" % (self.count, in_url))
            page_source = self.downloader.getPageSourceViaRequest(in_url)
            data = self.parser.parseHero(page_source)
            self.outputer.collectData(data)
            self.count += 1

        raw_html = self.downloader.downloadPageSource()
        new_urls, next_page_tag = self.parser.parse(raw_html, self.downloader.start_url)
        self.downloader.next_page_tag = next_page_tag
        self.url_manager.addNewUrl(new_urls)
        gainNewUrlsThread = Thread(target=parse_new_urls)
        gainNewUrlsThread.run()
        executor = tpe(self.thread_pool_size)
        while not self.url_manager.isEmpty():
            all_urls = self.url_manager.getUrls()
            executor.map(parse_detail, all_urls)
            if self.outputer.data_count > self.outputer.buffer_size:
                self.buffer_trigger.set()
        self.outputer.end_writing = True
        self.buffer_trigger.set()
        executor.shutdown(wait=True)






