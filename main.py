from crawl.crawler import Crawler

start_url = "http://stzb.163.com/card_list.html"
demo = Crawler(start_url)
demo.startCrawl()