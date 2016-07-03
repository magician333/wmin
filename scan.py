# coding:utf-8
# 本程序由紫火编写
# program by purplefire

from sys import version_info
import requests,socket
import result
from config import max_status_code,timeout,default_ua
import os

if version_info.major == 3:
    from printf.py3 import printf,printweb
else:
    from printf.py2 import printf,printweb


def web_deal(web):

    if web.startswith("http://"):
        prweb = web
        without_web = web[7:]
    elif web.startswith("https://"):
        prweb = web
        without_web = web[8:]
    else:
        prweb = "http://" + web
        without_web = web

    if web.endswith("/"):
        prweb = web[:-1]
        without_web = web[:-1]
    else:
        #prweb = web
        pass
    return prweb,without_web

def get_info(web,timeout=timeout,proxy=None,ua=None):
    try:
        printf("Server:\t"+requests.get(web_deal(web)[0],timeout=timeout,proxies=proxy,headers=None).headers["Server"],"normal")
    except:
        printf("Can\'t get server,Connect wrong","error")
    try:
        printf("IP:\t"+socket.gethostbyname(web_deal(web)[1]),"normal")
    except:
        printf("Can\'t get ip,Connect wrong","error")



def scan(web, dictionary, export_filename="", to=0.4, proxy=None,ua=None,ignore_text=""):
    web = web_deal(web)[0]
    web_length = len(web)

    for line in open(dictionary).readlines():
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



def urls_scan(urls, dictionary_loc, timeout=0.4, proxy=None,ua=None,ignore_text=""):
    for url in open(urls).readlines():
        scan(url.strip("\n"), dictionary_loc, result.init_webframe(None,url.strip("\n")), to=timeout, proxy=proxy,ua=ua,ignore_text=ignore_text)



def dicts_scan(url, dict_folder, result_filename, timeout=0.4, proxy=None,ua=None,ignore_text=""):
    for dictionary in os.listdir(dict_folder):
        scan(url, dict_folder+"/"+dictionary, result_filename, to=timeout, proxy=proxy,ua=ua,ignore_text=ignore_text)



def dicts_urls_scan(urls, dict_folder, result_filename, timeout=0.4, proxy=None,ua=None,ignore_text=""):
    for url in open(urls).readlines():
        for dictionary in os.listdir(dict_folder):
            scan(url.strip("\n"), dict_folder+"/"+dictionary,result.init_webframe(None,url), to=timeout, proxy=proxy,ua=ua,ignore_text=ignore_text)


