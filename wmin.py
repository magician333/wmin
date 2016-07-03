import argparse
import os
import scan
import result
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

def build_result(string,url):
    if string == None:
        filename = scan.web_deal(url)[1]
    else:
        filename = string
    return result.init_webframe(filename)

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
def build_nts(string):
    if string == None:
        return ""
    else:
        return string


if __name__ == "__main__":
    arg = argparse.ArgumentParser(description="Website Miner(网站矿工)")

    arg.add_argument("-u",type=str,help="set target url")
    arg.add_argument("-U",type=str,help="set urls file")
    arg.add_argument("-d",type=str,help="set dictionary")
    arg.add_argument("-D",type=str,help="set dictionary folder")
    arg.add_argument("-r",type=str,help="set report filename")
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
    timeout = para["t"]
    proxy = build_proxy(para["p"])
    ua = build_ua(para["a"])
    ignore_text = build_nts(para["i"])


    if (url and urls) or (dictionary and dictionarys):
        printf("Parameter make an error,just support a kind of set function","error")
    elif urls and para["r"]:
        printf("If you set URLS,you can not set the output filename","error")
    else:
        if url and dictionary == "" and dictionarys == None:
            scan.get_info(url, timeout, proxy, ua)
        elif urls and dictionary == "" and dictionarys == None:
            scan.gets_info(urls, timeout, proxy, ua)
        elif url and dictionary:
            scan.scan(url, dictionary, result.init_webframe(para["r"], url), timeout, proxy, ua, ignore_text)
        elif urls and dictionary:
            scan.urls_scan(urls, dictionary, timeout, proxy, ua, ignore_text)
        elif url and dictionarys:
            scan.dicts_scan(url, dictionarys, result.init_webframe(para["r"],url), timeout, proxy, ua, ignore_text)
        elif urls and dictionarys:
            scan.dicts_urls_scan(urls, dictionarys, timeout, proxy, ua, ignore_text)
