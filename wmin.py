import argparse
from libs import addon
from sys import version_info
from libs import Url
if version_info.major == 3:
    from libs.printf.py3 import printf, printweb
    from urllib.parse import urlparse
else:
    from libs.printf.py2 import printf, printweb
    from urlparse import urlparse


def main():

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
    # arg.add_argument("-r", type=str, help="set report filename", metavar="")
    arg.add_argument("-t", type=float, help="set timeout",
                     metavar="", default=0.04)
    arg.add_argument("-p", type=str,
                     help="set proxy    *format:  ip:port@type",
                     default="", metavar="")
    arg.add_argument("-P", type=str,
                     help="set proxy file,random read", default="", metavar="")
    arg.add_argument("-m", type=str,
                     help="set method", default="get", metavar="")
    arg.add_argument("-e", type=int,
                     help="set delay seconds", default=0, metavar="")
    arg.add_argument("-a", type=str,
                     help="set User-Agent", metavar="", default="")
    arg.add_argument("-A", type=str,
                     help="set User-Agent file,random read",
                     default="", metavar="")
    arg.add_argument("-x", type=int,
                     help="set multithreading number", default=1, metavar="")
    arg.add_argument("-X", type=int,
                     help="set multiprocessing number", default=1, metavar="")
    arg.add_argument("-i", type=str,
                     help="set ignore text", default='404', metavar="")

    args = arg.parse_args()
    para = vars(args)

    url = addon.deal_url(para["u"], para["U"])
    dictionary = addon.deal_dict(para["d"], para["D"])
    # report = addon.deal_report(para["r"])
    timeout = addon.deal_num(para["t"])
    proxy = addon.batch_deal(para["p"], para["P"])
    delay = addon.deal_num(para["e"])
    ua = addon.batch_deal(para["a"], para["A"])
    ignore_text = para["i"]
    method = addon.filter_method(para["m"])

    # if url.qsize() > 1 and report:
    #    printf("If you set URLS,you can not set the output filename", "error")
    # else:

    if url and dictionary is None:
        for i in range(url.qsize()):
            target = Url.Url(url.get(), "", timeout,
                             proxy, delay, ua, ignore_text, method)
            target.get_info()
    elif url and dictionary:
        for i in range(url.qsize()):
            target = Url.Url(url.get(), dictionary,
                             timeout, proxy, delay, ua, ignore_text, method)
            target.build_report_file()
            target.run()


if __name__ == '__main__':

    try:
        main()
    except:
        printf("Maybe something wrong.........\n", "warning")
        exit()
