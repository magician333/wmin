# coding=utf-8

import time
import queue
import requests
import socket

from . import report
from random import randint
from .display import printf, printweb
from urllib.parse import urlparse
from .config import *
from requests.packages import urllib3


class Net:
    """Url is the most important part of wmin,
    this class include the scan and get website information"""

    def __init__(self, domain, dictionary, timeout,
                 proxy, delay, ua, ignore_text, method, ssl):
        self.format_url(domain)
        self.dictionary = self.format_dict(dictionary)
        self.timeout = timeout
        self.proxy = list(map(self.set_proxy, proxy))
        self.ua = list(map(self.set_ua, ua))
        self.delay = delay
        self.ignore_text = ignore_text
        self.method = self.filter_method(method)
        self.fail_url = queue.Queue()
        self.ssl = ssl

    def set_ua(self, ua):
        if "" == ua:
            return None
        else:
            return dict({"User-Agent": ua})

    def set_proxy(self, proxy):
        if "" != proxy:
            if ":" and "@" in proxy:
                # proxy type : ip:port@type
                proxy = dict({proxy.split("@")[1]: proxy.split(":")[0]
                              + ":" + proxy.split("@")[0].split(":")[1]})
                return proxy
            else:
                printf("Type wrong!", "warning")
                return None
        else:
            return None

    def set_reportfile(self):
        self.report_filename = report.init_html(self.hostname)

    def format_dict(self, dictionary):
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
            except UnicodeDecodeError:
                printf("Coding error,please convert file to utf-8", "error")
                exit()
            except FileNotFoundError:
                self.dict_line = None

        if isinstance(dictionary, list):
            # dictionarys folder list
            for filename in dictionary:
                add_dictline(filename)
        else:
            # single dictionary file
            add_dictline(dictionary)

    def format_url(self, url):
        protocol = urlparse(url).scheme
        if protocol:
            purl = url
            hostname = urlparse(url).netloc

            if url.endswith("/"):
                purl = url[:-1]
                hostname = url[:-1]

            self.domain = purl
            self.hostname = hostname
        else:
            printf("Please enter url with protocl", "warning")
            exit()

    def filter_method(self, method):
        if method.lower() not in ["get", "post", "head"]:
            return None
        else:
            return method.lower()

    def scan(self):
        url = self.domain + self.dict_line.get_nowait()

        urllib3.disable_warnings  # disable ssl verify warnings

        try:
            # use appoint method
            kwargs = {"url": url,
                      "timeout": self.timeout,
                      "proxies": self.proxy[randint(0, len(self.proxy)-1)],
                      "headers": self.ua[randint(0, len(self.ua)-1)],
                      "verify": self.ssl,
                      "allow_redirects": False}

            if "get" == self.method:
                response = requests.get(**kwargs)
            elif "post" == self.method:
                response = requests.post(**kwargs)
            else:
                response = requests.head(**kwargs)

            code = response.status_code
            html = response.text

            if "" != self.ignore_text and "head" == self.method:
                printf("Can't use head method and ignore text at the same time",
                       "error")
                exit()

            if self.ignore_text == "" or self.ignore_text not in html:
                if code not in ignore_display_status_code:
                    printweb(code, url)
                if code not in ignore_report_status_code:
                    report.export_html(self.report_filename,
                                       url, url+"&nbsp;&nbsp;&nbsp;<strong>[" + str(code)+"]</strong>")

        except KeyboardInterrupt:
            exit()
        except Exception as e:
            self.fail_url.put(url.replace(self.domain, ""))
            printf(url + "\tConnect error", "error")
        time.sleep(self.delay)
        # delay time

    def reconnect(self):
        while 0 != self.fail_url.qsize():
            try:
                if input("Reconnect failed url?[Y/n]") in [
                        "n", "no", "No", "NO"]:
                    break
                else:
                    self.dict_line = self.fail_url
                    self.fail_url = queue.Queue()
                    self.run()
            except:
                exit()

    def get_info(self):

        printf("\n")
        printf("Domain:\t" + self.domain, "normal")
        try:
            try:
                printf("Server:\t" + requests.get
                       (self.domain, timeout=self.timeout,
                        proxies=self.proxy[
                            randint(0, len(self.proxy)-1)],
                        headers=self.ua[randint(0, len(self.ua)-1)],
                        allow_redirects=False).headers["Server"], "normal")

            except:
                printf("Can\'t get server,Connect wrong", "error")
            try:
                printf("IP:\t" +
                       socket.gethostbyname(self.hostname), "normal")
            except:
                printf("Can\'t get ip,Connect wrong", "error")
            printf("")
        except KeyboardInterrupt:
            exit()

    def run(self):

        stime = time.time()
        topprompt = "Total number of dictionary:"+str(self.dict_line.qsize())

        printf("\n")
        printf(topprompt, "normal")
        printf("")

        for i in range(self.dict_line.qsize()):
            self.scan()

        bottomprompt = "All works done! It takes " + \
            str(time.time()-stime)[:5]+"s"
        printf("")
        printf(bottomprompt, "normal")
        printf("The report file has been saved \"./" +
               self.report_filename+"\"", "normal")
