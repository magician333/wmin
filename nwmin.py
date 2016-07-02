import argparse
import os
import scan
from sys import version_info
from config import timeout,default_ua

if version_info.major == 3:
    from printf.py3 import printf
else:
    from printf.py2 import printf

def check_dic(dic):
    if dic != None:
        try:
            open(dic)
            return dic
        except FileNotFoundError:
            printf("Dictionary not found","error")
            return None
    else:
        return ""

def build_nts(string):
    if string == None:
        return ""
    else:
        return string

def build_proxy(proxy=None):
    if proxy != None:
        if ":" and "~" in proxy:
            proxy = dict({argv[i+1].split("~")[1]: argv[i+1].split(":")[0]+":"+argv[i+1].split("~")[0].split(":")[1]})
            return proxy
        else:
            printf("Type wrong!","warning")
            return None
    else:
        return None

def build_ua(ua=None):
    if ua != None:
        ua = {"User-Agent":ua}
        return ua
    else:
        ua = {"User-Agent":default_ua}
        return ua

def get_urls(urls):
    if urls != None:
        if os.path.isfile(urls):
            return urls
        else:
            printf("Urls file not exists!","error")
            return None
    else:
        return None

def get_dicts(dicts):
    if dicts != None:
        if os.path.isdir(dicts):
            return dicts
        else:
            printf("Dictionary folder not exists!","warning")
            return None
    else:
        return None

if __name__ == "__main__":
    arg = argparse.ArgumentParser()

    arg.add_argument("-u",type=str,help="set target url")
    arg.add_argument("-U",type=str,help="set urls file")
    arg.add_argument("-d",type=str,help="set dictionary")
    arg.add_argument("-D",type=str,help="set dictionary folder")
    arg.add_argument("-f",type=str,help="set output filename")
    arg.add_argument("-t",type=float,help="set timeout")
    arg.add_argument("-p",type=str,help="set proxy    *format:  ip:port~type")
    arg.add_argument("-m",type=int,help="set mutliprogress    *No development now")
    arg.add_argument("-a",type=str,help="set User-Agent")
    arg.add_argument("-i",type=str,help="set ignore text")

    args = arg.parse_args()
    para = vars(args)

    url = para["u"]
    urls = get_urls(para["U"])
    dictionary = check_dic(para["d"])
    dictionarys = get_dicts(para["D"])
    result_file = build_nts(para["f"])
    timeout = para["t"]
    proxy = build_proxy(para["p"])
    ua = build_ua(para["a"])
    ignore_text = build_nts(para["i"])


    if url and urls:
        printf("Parameter make an error,just support a kind of set url function","error")
    else:
        if url and dictionary:
            scan.dic_scan(url, dictionary, result_file, timeout, proxy,ua,ignore_text)
        elif url and dictionary == "":
            scan.get_info(url,timeout,proxy,ua)
        elif urls and dictionary:
            scan.urls_scan(urls, dictionary, result_file, timeout, proxy,ua,ignore_text)
