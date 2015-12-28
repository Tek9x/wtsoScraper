import requests
import re
import js2py

class generate(object):
    def __init__(self, url):
        self.url = url

    def WebsiteDownload(self):
        header = {"Referer": "http://google.com/"}
        findeval = '(eval[^<]+)'
        yx = self.url
        s = requests.Session()
        ldo = s.get(yx, headers=header)
        eV = re.findall(findeval, ldo.content)[0]
        return eV

    def WebsiteEval(self):
        rr = '(\$\("\d"\).\d)'
        eV = self.WebsiteDownload()
        js = re.sub(rr, '', eV)
        downloadURL = js2py.eval_js(js)
        return downloadURL