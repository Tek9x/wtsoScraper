import requests
from bs4 import BeautifulSoup
from generate import generate


class WtsoScraper(object):
    def __init__(self):
        self.r = requests.get('http://www.wtso.cc/video/vic/eng/season_1?lang=en')
        self.data = self.r.text
        self.soup = BeautifulSoup(self.data, 'lxml')

    def get_urls(self):
        u = self.soup.select("div.entryBlock [href]")
        episodes = [link['href'] for link in u]
        return episodes

    def get_data(self):
        t = self.soup.select(".a1")
        whitespace = [self.sanitize(i) for i in t]
        titles = [x.strip(' ') for x in whitespace]
        m = self.soup.select('div.entryBlock [src]')
        images = [s['src'] for s in m]
        return titles, images

    def get_video(self):
        videos = []
        for i in self.get_urls():
            r = requests.get(i)
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            v = soup.find('iframe')['src']
            videos.append(str(v).rstrip('&width=980&height=430'))
        return videos

    def get_desc(self):
        description = []
        r = requests.get('http://www.imdb.com/title/tt0096697/episodes?season=1')
        data = r.text
        soup = BeautifulSoup(data, 'lxml')
        d = soup.select('div.item_description')
        whitespace = [self.sanitize(i) for i in d]
        # for i in range(0, len(whitespace), 1):
        # description.append(whitespace[i:i+1])
        return whitespace

    def get_mobile(self):
        mobile = [generate(i).WebsiteEval() for i in self.get_video()]
        return mobile

    def sanitize(self, lst):
        tags = lst.string.strip()
        sanitize = str(tags).lstrip('Season 1234567890 episode')
        final_t = str(sanitize).lstrip('-')
        return final_t

    def build(self):
        database = zip(self.get_data()[0], self.get_video(), self.get_data()[1], self.get_desc(), self.get_mobile())
        return database


abc = WtsoScraper()
print abc.build()[0]

if __name__ == '__main__':
    start = WtsoScraper()
