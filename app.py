# -*- coding: utf-8 -*-

import requests, json
from bs4 import BeautifulSoup
from generate import generate
from util import save_file
from pprint import pprint
from collections import OrderedDict




class WtsoScraper(object):
    def __init__(self):
        self.r = requests.get('http://www.wtso.cc/video/vic/eng/season_23?lang=en')
        self.data = self.r.text
        self.soup = BeautifulSoup(self.data, 'lxml')

    def get_urls(self):
        print '[debug]: Starting [get_urls] function'
        u = self.soup.select("div.entryBlock [href]")
        episodes = [link['href'] for link in u]
        return episodes

    def get_data(self):
        print '[debug]: Starting [get_data] function'
        t = self.soup.select(".a1")
        whitespace = [self.sanitize(i) for i in t]
        titles = [x.strip(' ') for x in whitespace]
        m = self.soup.select('div.entryBlock [src]')
        images = [s['src'] for s in m]
        return titles, images

    def get_video(self):
        videos = []
        print '[debug]: Starting [get_video] function'
        for i in self.get_urls():
            r = requests.get(i)
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            v = soup.find('iframe')['src']
            videos.append(v)
        return videos

    def get_desc(self):
        print '[debug]: Starting [get_desc] function'
        description = []
        r = requests.get('http://www.imdb.com/title/tt0096697/episodes?season=23')
        data = r.text
        soup = BeautifulSoup(data, 'lxml')
        d = soup.select('div.item_description')
        whitespace = [self.sanitize(i) for i in d]
        # for i in range(0, len(whitespace), 1):
        # description.append(whitespace[i:i+1])
        return whitespace

    def get_mobile(self):
        print '[debug]: Starting [get_mobile] function'
        mobile = [generate(i).WebsiteEval() for i in self.get_video()]
        return mobile

    @staticmethod
    def sanitize(lst):
        tags = lst.string.strip()
        sanitize = tags.lstrip('Season 1234567890 episode')
        final_t = sanitize.lstrip('-')
        return final_t

    def build(self):
        print '[debug]: Starting [building] function'
        #database = zip(self.get_data()[0], self.get_video(), self.get_data()[1], self.get_desc(),self.get_mobile())
        database = {"Episodes":[{"title":a,"url":b,"thumb":c,"mobile":d} for a,b,c,d in zip(self.get_data()[0],self.get_video(),self.get_data()[1], self.get_mobile())]}
        save_file(database,'data/Season_23.json')


abc = WtsoScraper()
abc.build()

if __name__ == '__main__':
    start = WtsoScraper()
