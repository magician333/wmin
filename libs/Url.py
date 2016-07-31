#coding : utf-8

import queue


if version_info.major == 3:
    from .printf.py3 import printf
    from urllib.parse import urlparse
else:
    from .printf.py2 import printf
    from urlparse import urlparse


class Url:
    """docstring for Url"""
    def __init__(self, url,dictionary,timeout,proxy,delay,ua,ignore_text,method):
        super(Url, self).__init__()
        self.url = url
        self.dictionary = dic
        self.timeout = timeout
        self.proxy = build_proxy(proxy)
        self.delay = delay
        self.ua = build_ua(ua)
        self.ignore_text = ignore_text
        self.method = filter_method(method)


    def deal_dictionary(self):
        self.dict_line = queue.Queue()
        try:
            with open(self.dictionary) as dic:
                for line in dic.readlines():
                    if not line.startswith("//"):
                        self.dict_line.put(line.strip("\n"))
        except FileNotFoundError:
            self.dict_line = None

    def url_deal(self):
        protocol = urlparse(url).scheme
        if protocol:
            purl = url
            hostname = urlparse(url).netloc
            if url.endswith("/"):
                purl = url[:-1]
                hostname = url[:-1]
            else:
                pass
            self.purl = purl
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
                    # proxy : ip:port@type
                    proxy = dict({proxy.split("@")[1]: proxy.split(":")[
                                 0] + ":" + proxy.split("@")[0].split(":")[1]})
                    return proxy
                else:
                    printf("Type wrong!", "warning")
                    return None
            else:
                return None

    def build_ua(self,ua):
        if None != ua:
            ua = {"User-Agent": ua}
        else:
            ua = {"User-Agent": default_ua}
        return ua