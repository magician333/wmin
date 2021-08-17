# coding=utf-8
import argparse
from libs import addon, Url
from thirdparty import colorama
from libs.display import printf


def main():
    colorama.init()
    banner = """
                            ██              
                            ▀▀               | dev <0.10> |
    ██      ██  ████▄██    ████     ██▄████ 
    ▀█  ██  █▀  ██ ██ ██     ██     ██▀   ██ 
     ██▄██▄██   ██ ██ ██     ██     ██    ██ 
     ▀██  ██▀   ██ ██ ██  ▄▄▄██▄▄▄  ██    ██ 
      ▀▀  ▀▀    ▀▀ ▀▀ ▀▀  ▀▀▀▀▀▀▀▀  ▀▀    ▀▀ """
    usage = "wmin.py -u url [options]"
    description = '''
    Wmin is a web content discovery tool.
    It make requests and analyze the responses trying to figure out whether the
    resource is or not accessible.
    '''
    epilog = "License, requests, etc: https://github.com/magician333/wmin"
    arg = argparse.ArgumentParser(usage=usage,
                                  description=description, epilog=epilog)
    printf(colorama.Fore.LIGHTBLUE_EX+banner+colorama.Fore.RESET)
    arg.add_argument(
        "-u", type=str, help="set target url, must with protocl", metavar="")
    arg.add_argument("-U", type=str, help="set urls file", metavar="")
    arg.add_argument(
        "-d", type=str, help="set dictionary, best to use txt format", metavar="")
    arg.add_argument("-D", type=str, help="set dictionary folder", metavar="")
    # arg.add_argument("-r", type=str, help="set report filename", metavar="")
    arg.add_argument("-t", type=float, help="set timeout",
                     metavar="", default=0.4)
    arg.add_argument("-p", type=str,
                     help="set proxy    *format:  ip:port@type, like 0.0.0.0@http",
                     default="", metavar="")
    arg.add_argument("-P", type=str,
                     help="set proxy file,random read", default="", metavar="")
    arg.add_argument("-m", type=str,
                     help="set method, GET POST HEAD or others, default GET", default="get", metavar="")
    arg.add_argument("-e", type=int,
                     help="set delay seconds, default 0", default=0, metavar="")
    arg.add_argument("-a", type=str,
                     help="set User-Agent", metavar="", default="")
    arg.add_argument("-A", type=str,
                     help="set User-Agent file,random read",
                     default="", metavar="")
    arg.add_argument("-i", type=str,
                     help="set ignore text", default="", metavar="")

    args = arg.parse_args()
    para = vars(args)

    url = addon.format_urls(para["u"], para["U"])
    dictionary = addon.format_dicts(para["d"], para["D"])
    timeout = addon.format_nums(para["t"])
    proxy = addon.format_batchs(para["p"], para["P"])
    delay = addon.format_nums(para["e"])
    ua = addon.format_batchs(para["a"], para["A"])
    ignore_text = para["i"]
    method = addon.filter_method(para["m"])

    if "" != ignore_text and "head" == method:
        printf("Can't use head method and ignore text at same time",
               "error")
        exit()

    if url and dictionary is None:
        for i in range(url.qsize()):
            target = Url.Url(url.get(), "", timeout,
                             proxy, delay, ua, ignore_text, method)
            target.get_info()
    elif url and dictionary:
        for i in range(url.qsize()):
            target = Url.Url(url.get(), dictionary,
                             timeout, proxy, delay, ua, ignore_text, method)
            target.set_reportfile()
            target.run()
            target.reconnect()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # if you want to show the details of error
        print(e)
        if False:

            printf("Maybe something wrong.........\n", "warning")
            exit()
