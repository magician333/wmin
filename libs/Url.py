#coding : utf-8

import queue
import time
import requests
import threading
import ipdb
import random
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
        self.url_deal(url)
        self.dictionary = self.deal_dictionary(dictionary)
        self.timeout = timeout
        self.proxy = list(map(self.build_proxy,proxy))
        self.ua = list(map(self.build_ua,ua))
        self.delay = delay
        self.ignore_text = ignore_text
        self.method = self.filter_method(method)
        ipdb.set_trace()

    def deal_dictionary(self,dictionary):
        self.dict_line = queue.Queue()

        def add_dictline(filename):
            try:
                with open(filename) as dic:
                    for line in dic.readlines():
                        if not line.startswith("#"):
                            # allow use '#' as note
                            if line.startswith("/"):
                                self.dict_line.put(line.strip("\n"))
                            else:
                                self.dict_line.put("/" + line.strip("\n"))
            except FileNotFoundError:
                self.dict_line = None


        if isinstance(dictionary,list):
            #dictionarys folder list
            for filename in dictionary:
                add_dictline(filename)
        else:
            #single dictionary file
            add_dictline(dictionary)


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

    def build_ua(self,ua):
        if "" == ua:
            return None
        else:
            return dict({"User-Agent": ua})
    def build_proxy(self,proxy):
        if "" != proxy:
            if ":" and "@" in proxy:
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
        url = self.url + self.dict_line.get_nowait()

        time.sleep(self.delay)
        # delay time
            
        try:
            # use appoint method
            if "get" == self.method:
                code = requests.get(url, timeout=self.timeout, proxies=self.proxy[random.randint(0,len(self.proxy)-1)], headers=self.ua[random.randint(0,len(self.ua)-1)], allow_redirects=False).status_code
            elif "post" == self.method:
                code = requests.post(url, timeout=self.timeout, proxies=self.proxy[random.randint(0,len(self.proxy)-1)],headers=self.ua[random.randint(0,len(self.ua)-1)], allow_redirects=False).status_code
            else:
                code = requests.head(url, timeout=self.timeout, proxies=self.proxy[random.randint(0,len(self.proxy)-1)],headers=self.ua[random.randint(0,len(self.ua)-1)], allow_redirects=False).status_code

            if "" != self.ignore_text and self.ignore_text not in requests.get(url).text:
                printweb(code, url)
                if code < 400:
                    result.export_result(self.report_filename, url, url + "\t" + str(code))
            self.dict_line.task_done()
        except KeyboardInterrupt:
            exit()
        except:
            printf(url + "\tConnect error", "error")

    def run(self):
        for i in range(self.dict_line.qsize()):
            self.scan()