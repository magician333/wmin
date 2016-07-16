import socket
from thirdparty import requests
from . import addon
from .config import timeout,default_ua
from sys import version_info

if version_info.major == 3:
    from .printf.py3 import printf
else:
    from .printf.py2 import printf


def get_info(web,timeout=timeout,proxy=None,ua=None):

    printf("Domain:\t"+addon.web_deal(web)[0],"normal")
    
    if type(ua) == str:
        ua = addon.build_ua(addon.get_random_line(ua),None)
    if type(proxy) == str:
        proxy = addon.build_proxy(addon.get_random_line(proxy),None)  

    try:
        printf("Server:\t"+requests.get(addon.web_deal(web)[0],timeout=timeout,proxies=proxy,headers=ua).headers["Server"],"normal")
    except:
        printf("Can\'t get server,Connect wrong","error")
    try:
        printf("IP:    \t"+socket.gethostbyname(addon.web_deal(web)[1]),"normal")
    except Exception as e:
        print(e)
        printf("Can\'t get ip,Connect wrong","error")
    printf("")

def gets_info(urls, timeout=timeout, proxy=None, ua=None):

    for url in open(urls).readlines():
        get_info(url.strip("\n"), timeout, proxy, ua)

