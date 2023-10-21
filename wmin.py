# coding=utf-8

import argparse

from libs import addon, net, report
from thirdparty import colorama
from libs.display import printf
from libs.config import *


def main():
    colorama.init()

    parser = argparse.ArgumentParser(usage=usage,
                                     description=description, epilog=epilog)

    printf(colorama.Fore.LIGHTBLUE_EX+banner+colorama.Fore.RESET)

    parser.add_argument(
        "-u", type=str, help="set domain, must with protocol", metavar="")
    parser.add_argument("-U", type=str, help="set domain file", metavar="")
    parser.add_argument("-d", type=str, help="set dictionary, best to use txt format",
                        default=default_dictionary, metavar="")
    parser.add_argument("-D", type=str, help="set dictionary folder",
                        default=default_Dictionaryfolder, metavar="")
    parser.add_argument("-t", type=float, help="set timeout",
                        metavar="", default=default_timeout)
    parser.add_argument(
        "-p", type=str, help="set proxy *format: ip:port@type, like 0.0.0.0:8080@http", default=default_proxy, metavar="")
    parser.add_argument(
        "-P", type=str, help="set proxy file, random read", default="", metavar="")
    parser.add_argument("-m", type=str, help="set method, GET POST HEAD or others, default GET",
                        default=default_method, metavar="")
    parser.add_argument(
        "-e", type=int, help="set delay seconds, default 0", default=0, metavar="")
    parser.add_argument("-a", type=str, help="set User-Agent",
                        default=default_ua, metavar="")
    parser.add_argument(
        "-A", type=str, help="set User-Agent file, random read", default="", metavar="")
    parser.add_argument("-i", type=str, help="set ignore text",
                        default=default_ignoretext, metavar="")
    parser.add_argument(
        "-s", type=str, help="set whether to use SSL", default=default_ssl, metavar="")

    args = parser.parse_args()
    para = vars(args)

    url = addon.format_urls(para["u"], para["U"])
    dictionary = addon.format_dicts(para["d"], para["D"])
    timeout = addon.format_nums(para["t"])
    proxy = addon.format_batchs(para["p"], para["P"])
    delay = addon.format_nums(para["e"])
    ua = addon.format_batchs(para["a"], para["A"])
    ignore_text = para["i"]
    method = addon.filter_method(para["m"])
    ssl = addon.read_file(para["s"])

    if url is not None and dictionary is None:
        while not url.empty():
            target = net.Net(url.get(), "", timeout, proxy,
                             delay, ua, ignore_text, method, ssl)
            target.get_info()
    elif url is not None and dictionary is not None:
        while not url.empty():
            target = net.Net(url.get(), dictionary, timeout,
                             proxy, delay, ua, ignore_text, method, ssl)
            target.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # if you want to show the details of error
        print(e)
