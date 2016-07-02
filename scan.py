# coding:utf-8
# 本程序由紫火编写
# program by purplefire

from sys import version_info
import requests,socket
import result
from config import max_status_code,timeout,default_ua
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




def dic_scan(web, dictionary, export_filename="", to=0.4, proxy=None,ua=None,ignore_text=""):
    if 0 == len(export_filename):
        export_filename = web_deal(web)[1]
    web = web_deal(web)[0]
    export_filename = result.initialize_webframe(export_filename)  # use result to create web form

    dic_f = open(dictionary)  # open dictionary
    line = dic_f.readline()
    web_length = len(web)

    while line:  # read one line by line
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
        line = dic_f.readline()
        if line == None:
            break




def urls_scan(urls, dictionary_loc, export_filename="", timeout=0.4, proxy=None,ua=None,ignore_text=""):
    for url in open(urls).readlines():
        dic_scan(url.strip("\n"), dictionary_loc, export_filename, to=timeout, proxy=proxy,ua=ua,ignore_text=ignore_text)
