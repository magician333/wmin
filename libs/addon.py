import os
import random
from .config import default_ua
from sys import version_info
import glob
import queue

if version_info.major == 3:
    from .printf.py3 import printf
    from urllib.parse import urlparse
else:
    from .printf.py2 import printf
    from urlparse import urlparse



def filter_method(method):
    if method.lower() not in ["get", "post", "head"]:
        printf("HTTP method error,must use get/post/head", "warning")
        return "get"
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
    else:
        list_.append("")
    
    return list_  

def deal_report(filename):
    for i in list(filename):
        if i in ["?", "`", "\\", "/", "*", "\"", "\'", "<", ">", "|"]:
            printf("You can not use forbidden character in filenam, especial on WINDOWS system!!!","error")
            break
            exit()
    return filename