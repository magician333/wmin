import os
import random
import linecache
from .config import default_ua
from sys import version_info

if version_info.major == 3:
    from .printf.py3 import printf
else:
    from .printf.py2 import printf


def get_random_line(filename):
    random_line = linecache.getline(filename, random.randint(
        1, len(open(filename).readlines()))).strip("\n")
    return random_line


def web_deal(url):

    if url.startswith("http://"):
        prurl = url
        without_url = url[7:]
    elif url.startswith("https://"):
        prurl = url
        without_url = url[8:]
    else:
        prurl = "http://" + url
        without_url = url

    if url.endswith("/"):
        prurl = url[:-1]
        without_url = url[:-1]
    else:
        #prweb = web
        pass
    return prurl, without_url


def filter_method(method):
    if method.lower() not in ["get", "post", "head"]:
        return None
    else:
        return method.lower()


def check_dic(dic):
    if dic != None:
        try:
            open(dic)
            return dic
        except FileNotFoundError:
            printf("Dictionary not found", "error")
            return None
    else:
        return ""


def build_result(string, url):
    if string == None:
        filename = addon.web_deal(url)[1]
    else:
        filename = string
    return result.init_webframe(filename)


def build_proxy(proxy, proxys):
    if proxy != None and proxys != None:
        printf("Parameter make an error,just support a kind of set function", "error")
        exit()
    else:
        if proxys == None:
            if proxy != None:
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
        else:
            return proxys


def build_ua(ua, uas):
    if ua != None and uas != None:
        printf("Parameter make an error,just support a kind of set function", "error")
        exit()
    else:
        if uas == None:
            if ua != None:
                ua = {"User-Agent": ua}
            else:
                ua = {"User-Agent": default_ua}
            return ua
        else:
            return uas


def test_file(filename):
    if filename != None:
        if os.path.isfile(filename):
            return filename
        else:
            printf(filename + " not exists!", "error")
            exit()
            return None
    else:
        return None


def test_dicts(dicts):
    if dicts != None:
        if os.path.isdir(dicts):
            return dicts
        else:
            printf("Dictionary folder not exists", "error")
            return None
    else:
        return None
