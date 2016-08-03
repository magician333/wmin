import os
import random
import linecache
from .config import default_ua
from sys import version_info
import glob
import queue
import ipdb

if version_info.major == 3:
    from .printf.py3 import printf
    from urllib.parse import urlparse
else:
    from .printf.py2 import printf
    from urlparse import urlparse


def get_random_line(filename):
    random_line = linecache.getline(filename, random.randint(
        1, len(open(filename).readlines()))).strip("\n")
    return random_line


def web_deal(url):

    protocol = urlparse(url).scheme
    if protocol:
        purl = url
        hostname = urlparse(url).netloc
        if url.endswith("/"):
            purl = url[:-1]
            hostname = url[:-1]
        else:
            pass
        return purl, hostname
    else:
        printf("Please enter url with protocl","error")
        exit()


def filter_method(method):
    if method.lower() not in ["get", "post", "head"]:
        return None
    else:
        return method.lower()


def deal_dict(dic,DIC):
    if dic and DIC:
        printf("Parameter make an error,just support a kind of set function", "error")
        exit()
    elif None == dic and None != DIC:
        if os.path.isdir(DIC):
            dictionary = glob.glob(DIC+"/*.*")
            return dictionary
        else:
            printf("Dictionary folder not exists", "error")
            exit()
    elif None != dic and None == DIC:
        try:
            open(dic)
            return dic
        except:
            printf("Dictionary not found", "error")
            exit()

def deal_url(url,URL):

    url_list = queue.Queue()
    if url and URL:
        printf("Parameter make an error,just support a kind of set function", "error")
        exit()
    elif None == url and URL != None:
        if os.path.isfile(URL):
            with open(URL) as f:
                for line in f.readlines():
                    url_list.put(line.strip("\n"))
        else:
            printf(filename + " not exists!", "error")
            exit()
    elif None != url and None == URL:
        url_list.put(url)
    return url_list

def batch_deal(single,mutile):
    #
    #
    #
    list_ = []
    if single and mutile:
        printf("Parameter make an error,just support a kind of set function", "error")
        exit()
    elif "" == single and mutile != "":
        if os.path.isfile(mutile):
            with open(mutile) as f:
                for line in f.readlines():
                    list_.append(line.strip("\n"))
        else:
            printf(filename + " not exists!", "error")
            exit()
    elif "" != single and "" == mutile:
        list_.append(single)
    
    return list_  


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



# def test_dicts(dicts):
#     if dicts != None:
#         if os.path.isdir(dicts):
#             return dicts
#         else:
#             printf("Dictionary folder not exists", "error")
#             return None
#     else:
#         return None
