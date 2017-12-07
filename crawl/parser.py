from bs4 import BeautifulSoup
from urllib import request
import re

class Parser:

    def __init__(self):
        pass

    def parse(self, raw_html, url_in = None):
        soup = BeautifulSoup(raw_html, 'html.parser', from_encoding="utf-8")
        hero_pool = soup.find("ul", class_="pic-list clearfix")
        hero_profiles = hero_pool.find_all("li")
        hero_urls = list()
        for i in range(len(hero_profiles)-1):
            raw_url = hero_profiles[i].a['href']
            hero_urls.append(request.urljoin(url_in, raw_url))
        next_page_tag = hero_profiles[-1].a.text
        return hero_urls, next_page_tag

    def parseHero(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser', from_encoding="GBK")
        body = soup.find("div", class_="wrap")
        basic_info = body.h1.text
        name, country, kind = basic_info.strip(" ").split("-")
        image_address = soup.find("span", class_="role-img").img['src']
        description = body.find('p', class_="desc").text.strip()
        description = description.replace("\n", "").replace("\r", "")
        attributes = body.find_all("p", class_="attr-list")
        data_list = list()       #cost, attack_range, ruse, attack, seige, defand, speed
        for attribute in attributes:
            for span in attribute.find_all("span"):
                res = re.search("[\d.]+", span.text)
                if res is None:
                    continue
                res = res.group()
                if "." in res:
                    data_list.append(float(res))
                else:
                    data_list.append(int(res))
        raw_skills = body.find_all("dl", class_="group")
        if len(raw_skills) == 1:
            carry_skill = raw_skills.text.replace(" ", "").replace("\n", "")[0][5::]
            decomposable_skill = "无"
        else:
            skills = list()
            for item in raw_skills:
                skills.append(item.text.replace(" ", "").replace("\n", ""))
            carry_skill = skills[0][5::]
            decomposable_skill = skills[-1][5::]
