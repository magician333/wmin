# coding=utf-8

import os
import glob
import queue

from .display import printf


def filter_method(method):
    if method.lower() not in ["get", "post", "head"]:
        printf("HTTP method error,must use get/post/head", "warning")
        return "get"
    else:
        return method.lower()


def format_dicts(dic, DIC):
    if dic and DIC:
        printf("Parameter error,just support a kind of set function", "error")
        exit()
    elif dic is None and DIC is not None:
        if os.path.isdir(DIC):
            dictionary = glob.glob(DIC+"/*.*")
            return dictionary
        else:
            printf("Dictionary folder not exists", "error")
            exit()
    elif dic is not None and DIC is None:
        try:
            open(dic)
            return dic
        except:
            printf("Dictionary not found", "error")
            exit()


def format_urls(url, URL):

    url_list = queue.Queue()
    if url and URL:
        printf("Parameter error,just support a kind of set function", "error")
        exit()
    elif url is None and URL is not None:
        if os.path.isfile(URL):
            try:
                with open(URL) as f:
                    for line in f.readlines():
                        url_list.put(line.strip("\n"))
            except UnicodeDecodeError:
                printf("Coding error,please convert file to utf-8", "error")
                exit()
        else:
            printf(URL + " not exists!", "error")
            exit()
    elif url is not None and URL is None:
        url_list.put(url)
    return url_list


def format_batchs(single, mutile):
    list_ = []
    if single and mutile:
        printf("Parameter error,just support a kind of set function", "error")
        exit()
    elif "" == single and mutile != "":
        if os.path.isfile(mutile):
            try:
                with open(mutile) as f:
                    for line in f.readlines():
                        list_.append(line.strip("\n"))
            except UnicodeDecodeError:
                printf("Coding error,please convert file to utf-8", "error")
                exit()
        else:
            printf(mutile + " not exists!", "error")
            exit()
    elif "" != single and "" == mutile:
        list_.append(single)
    else:
        list_.append("")

    return list_


def format_nums(num):
    if num < 0:
        printf("You must set a postive number,already convert plus", "warning")
        return abs(num)
    else:
        return num
