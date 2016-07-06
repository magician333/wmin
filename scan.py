# coding:utf-8

from sys import version_info
import requests
import result
import addon
from config import max_status_code,timeout
import os

if version_info.major == 3:
    from printf.py3 import printf,printweb
else:
    from printf.py2 import printf,printweb

def scan(web, dictionary, export_filename="", to=0.4, proxy=None,ua=None,ignore_text=""):
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
            ua = addon.build_ua(addon.get_random_line(uas),None)
        if type(proxys) == str:
            proxy = addon.build_proxy(addon.get_random_line(proxys),None)  

        
        line = line.strip('\n')  # remove the line feed


        if line.startswith("/"):
            web = web + line
        else:
            web = web + "/" + line
        try:

            def output(code,web):
                printweb(code,web)
                if code < max_status_code:
                    result.export_result(export_filename, web,web+"\t"+str(code))


            code = requests.get(web, timeout=to,proxies=proxy,headers=ua).status_code
            if "" != ignore_text and ignore_text not in requests.get(web).text:
                output(code,web)
            elif "" == ignore_text:
                output(code,web)
            else:
                pass
        except KeyboardInterrupt:
            break
            exit()
        except:
            printf(web+"\t\t\tConnet wrong!!!","error")

        web = web[0:web_length]
    printf("")


def urls_scan(urls, dictionary_loc, timeout=0.4, proxy=None,ua=None,ignore_text=""):
    for url in open(urls).readlines():
        scan(url.strip("\n"), dictionary_loc, result.init_webframe(None,url.strip("\n")), to=timeout, proxy=proxy,ua=ua,ignore_text=ignore_text)



def dicts_scan(url, dict_folder, result_filename, timeout=0.4, proxy=None,ua=None,ignore_text=""):
    for dictionary in os.listdir(dict_folder):
        scan(url, dict_folder+"/"+dictionary, result_filename, to=timeout, proxy=proxy,ua=ua,ignore_text=ignore_text)



def dicts_urls_scan(urls, dict_folder, timeout=0.4, proxy=None,ua=None,ignore_text=""):
    for url in open(urls).readlines():
        for dictionary in os.listdir(dict_folder):
            scan(url.strip("\n"), dict_folder+"/"+dictionary,result.init_webframe(None,url.strip("\n")), to=timeout, proxy=proxy,ua=ua,ignore_text=ignore_text)

