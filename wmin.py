import argparse
import os
from libs import result
from libs import scan
from libs import get_info
from libs import addon
from sys import version_info

if version_info.major == 3:
    from libs.printf.py3 import printf
else:
    from libs.printf.py2 import printf


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
        elif url and dictionary:
            scan.scan(url, dictionary, result.init_webframe(
                para["r"], url), timeout, proxy, ua, ignore_text, method, delay)
        elif urls and dictionary:
            scan.urls_scan(urls, dictionary, timeout, proxy,
                           ua, ignore_text, method, delay)
        elif url and dictionarys:
            scan.dicts_scan(url, dictionarys, result.init_webframe(
                para["r"], url), timeout, proxy, ua, ignore_text, method, delay)
        elif urls and dictionarys:
            scan.dicts_urls_scan(urls, dictionarys, timeout,
                                 proxy, ua, ignore_text, method, delay)
