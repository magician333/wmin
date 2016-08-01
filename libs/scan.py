# coding:utf-8
import os
import time
from . import result
from . import addon
from sys import version_info,exit
from thirdparty import requests
from .config import max_status_code


if version_info.major == 3:
    from .printf.py3 import printf, printweb
else:
    from .printf.py2 import printf, printweb


def custom_request(url, to, proxy, ua, method):
    """custom request convient for request method"""
    if "get" == method:
        code = requests.get(url, timeout=to, proxies=proxy,
                            headers=ua).status_code
    elif "post" == method:
        code = requests.post(url, timeout=to, proxies=proxy,
                             headers=ua).status_code
    else:
        code = requests.head(url, timeout=to, proxies=proxy,
                             headers=ua).status_code
    return code


def scan(web, dictionary, export_filename, to, proxy, ua, ignore_text, method, delay):
    if type(ua) == str:
        uas = ua
    else:
        uas = None
    if type(proxy) == str:
        proxys = proxy
    else:
        proxys = None

    web = addon.web_deal(web)[0]
    web_length = len(web)
    for line in open(dictionary).readlines():
        
        if type(uas) == str:
            ua = addon.build_ua(addon.get_random_line(uas), None)
        if type(proxys) == str:
            proxy = addon.build_proxy(addon.get_random_line(proxys), None)

        line = line.strip('\n')  # remove the line feed

        if line.startswith("/"):
            web = web + line
        else:
            web = web + "/" + line
        try:

            def output(code, web):
                printweb(code, web)
                if code < max_status_code:
                    result.export_result(export_filename, web, web + "\t" + str(code))

            time.sleep(delay)
            code = custom_request(web, to, proxy, ua, method)

            if "" != ignore_text and ignore_text not in requests.get(web).text:
                output(code, web)
            elif "" == ignore_text:
                output(code, web)
            else:
                pass
        except KeyboardInterrupt:
            break
            exit()    
        except:
            printf(web + "\t\t\tConnet wrong!!!", "error")
        web = web[0:web_length]

def urls_scan(urls, dictionary_loc, timeout, proxy, ua, ignore_text, method, delay):
    for url in open(urls).readlines():
        scan(url.strip("\n"), dictionary_loc, result.init_webframe(None, url.strip("\n")),
             to=timeout, proxy=proxy, ua=ua, ignore_text=ignore_text, method=method, delay=delay)


def dicts_scan(url, dict_folder, result_filename, timeout, proxy, ua, ignore_text, method, delay):
    for dictionary in os.listdir(dict_folder):
        scan(url, dict_folder + "/" + dictionary, result_filename, to=timeout,
             proxy=proxy, ua=ua, ignore_text=ignore_text, method=method, delay=delay)


def dicts_urls_scan(urls, dict_folder, timeout, proxy, ua, ignore_text, method, delay):
    for url in open(urls).readlines():
        for dictionary in os.listdir(dict_folder):
            scan(url.strip("\n"), dict_folder + "/" + dictionary, result.init_webframe(None, url.strip("\n")),
                 to=timeout, proxy=proxy, ua=ua, ignore_text=ignore_text, method=method, delay=delay)
