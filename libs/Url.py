#coding : utf-8

import queue
import time
import requests
import threading
from . import result
from sys import version_info

if version_info.major == 3:
    from .printf.py3 import printf,printweb
    from urllib.parse import urlparse
else:
    from .printf.py2 import printf,printweb
    from urlparse import urlparse


class Url:
    """docstring for Url"""
    def __init__(self, url,dictionary,timeout,proxy,delay,ua,ignore_text,method):
        super(Url, self).__init__()
        self.url_deal(url)
        self.dictionary = dictionary
        self.timeout = timeout
        self.proxy = self.build_proxy(proxy)
        self.delay = delay
        self.ua = None # {"User-Agent": ua}
        self.ignore_text = ignore_text
        self.method = self.filter_method(method)
        self.lock = threading.Lock()
        self.deal_dictionary()

    def deal_dictionary(self):
        self.dict_line = queue.Queue()
        try:
            with open(self.dictionary) as dic:
                for line in dic.readlines():
                    if not line.startswith("#"):
                        # allow use '#' as note
                        if line.startswith("/"):
                            self.dict_line.put(line.strip("\n"))
                        else:
                            self.dict_line.put("/" + line.strip("\n"))
        except FileNotFoundError:
            self.dict_line = None

    def url_deal(self,url):
        protocol = urlparse(url).scheme
        if protocol:
            purl = url
            hostname = urlparse(url).netloc

            if url.endswith("/"):
                purl = url[:-1]
                hostname = url[:-1]

            self.url = purl
            self.hostname = hostname
        else:
            printf("Please enter url with protocl","warning")
            exit()

    def filter_method(self,method):
        if method.lower() not in ["get", "post", "head"]:
            return None
        else:
            return method.lower()

    def build_proxy(self,proxy):
        if None != proxy:
            if ":" and "~" in proxy:
                # proxy type : ip:port@type
                proxy = dict({proxy.split("@")[1]: proxy.split(":")[0] + ":" + proxy.split("@")[0].split(":")[1]})
                return proxy
            else:
                printf("Type wrong!", "warning")
                return None
        else:
            return None

    def build_report_file(self):
        self.report_filename = result.init_webframe(self.hostname)

    def scan(self):
        url = self.url + self.dict_line.get()

        time.sleep(self.delay)
        # delay time
            
        try:
            # use appoint method
            if "get" == self.method:
                code = requests.get(url, timeout=self.timeout, proxies=self.proxy).status_code
            elif "post" == self.method:
                code = requests.post(url, timeout=self.timeout, proxies=self.proxy,headers=self.ua).status_code
            else:
                code = requests.head(url, timeout=self.timeout, proxies=self.proxy,headers=self.ua).status_code

            self.lock.acquire()
            if "" != self.ignore_text and self.ignore_text not in requests.get(url).text:
                printweb(code, url)
                if code < 400:
                    result.export_result(self.report_filename, url, url + "\t" + str(code))
            self.lock.release()
            self.dict_line.task_done()

        except:
            printf(url + "\tConnect error", "error")

    def run(self):
        for i in range(100):
            t = threading.Thread(target=self.scan())
            t.setDaemon(True)
            t.start()

    