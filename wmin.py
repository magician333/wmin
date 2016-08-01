import argparse
import os
from libs import result
from libs import scan
from libs import get_info
from libs import addon
from sys import version_info
import threading
import queue
import time
import requests
if version_info.major == 3:
    from libs.printf.py3 import printf,printweb
    from urllib.parse import urlparse
else:
    from libs.printf.py2 import printf,printweb
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
        url = self.url + self.dict_line.get_nowait()

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
        for i in range(10):
            t = threading.Thread(target=self.scan())
            t.setDaemon(True)
            t.start()

if __name__ == "__main__":

    usage = "wmin.py -u url -d dictionary [options]"
    description = '''
    Wmin is a web content discovery tool.
    It makes requests and analyze the responses trying to figure out whether the
    resource is or not accessible.
    '''
    epilog = "License, requests, etc: https://github.com/magician333/wmin"
    arg = argparse.ArgumentParser(
        usage=usage, description=description, epilog=epilog)

    arg.add_argument("-u", type=str, help="set target url", metavar="")
    arg.add_argument("-U", type=str, help="set urls file", metavar="")
    arg.add_argument("-d", type=str, help="set dictionary", metavar="")
    arg.add_argument("-D", type=str, help="set dictionary folder", metavar="")
    arg.add_argument("-r", type=str, help="set report filename", metavar="")
    arg.add_argument("-t", type=float, help="set timeout", metavar="",default=0.04)
    arg.add_argument(
        "-p", type=str, help="set proxy    *format:  ip:port@type", metavar="")
    arg.add_argument(
        "-P", type=str, help="set proxy file,random read", metavar="")
    arg.add_argument("-m", type=str, help="set method",
                     default="get", metavar="")
    arg.add_argument("-e", type=int, help="set delay seconds",
                     default=0, metavar="")
    arg.add_argument("-a", type=str, help="set User-Agent", metavar="",default = "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.1667.0 Safari/537.36")
    arg.add_argument(
        "-A", type=str, help="set User-Agent file,random read", metavar="")
    arg.add_argument(
        "-i", type=str, help="set ignore text default 404", default='404', metavar="")

    args = arg.parse_args()
    para = vars(args)

    url = para["u"]
    urls = addon.test_file(para["U"])
    dictionary = addon.check_dic(para["d"])
    dictionarys = addon.test_dicts(para["D"])
    timeout = para["t"]
    proxys = addon.test_file(para["P"])
    proxy = addon.build_proxy(para["p"], proxys)
    delay = para["e"]
    uas = addon.test_file(para["A"])
    ua = addon.build_ua(para["a"], uas)
    ignore_text = para["i"]
    method = addon.filter_method(para["m"])

    if (url and urls) or (dictionary and dictionarys):
        printf("Parameter make an error,just support a kind of set function", "error")
    elif urls and para["r"]:
        printf("If you set URLS,you can not set the output filename", "error")
    elif method == None:
        printf("HTTP method error,must use get/post/head", "error")
    else:
        if url and dictionary == "" and dictionarys == None:
            get_info.get_info(url, timeout, proxy, ua)
        elif urls and dictionary == "" and dictionarys == None:
            get_info.gets_info(urls, timeout, proxy, ua)
        # elif url and dictionary:
        #     scan.scan(url, dictionary, result.init_webframe(
        #         para["r"], url), timeout, proxy, ua, ignore_text, method, delay)
        # elif urls and dictionary:
        #     scan.urls_scan(urls, dictionary, timeout, proxy,
        #                    ua, ignore_text, method, delay)
        # elif url and dictionarys:
        #     scan.dicts_scan(url, dictionarys, result.init_webframe(
        #         para["r"], url), timeout, proxy, ua, ignore_text, method, delay)
        # elif urls and dictionarys:
        #     scan.dicts_urls_scan(urls, dictionarys, timeout,
        #                          proxy, ua, ignore_text, method, delay)
        elif url and dictionary:
            target = Url(url,dictionary,timeout,proxy,delay,ua,ignore_text,method)
            target.build_report_file()
            while 1:
                if threading.activeCount() <= 1:
                    target.run()
                    break
                    exit()
            