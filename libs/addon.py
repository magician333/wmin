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
        printf("Parameter error, only one parameter of the same type can be set", "error")
        exit()
    elif dic is None and DIC is not None:
        if os.path.isdir(DIC):
            dictionary = glob.glob(os.path.join(DIC, "*.*"))
            return dictionary
        else:
            printf("Dictionary folder does not exist", "error")
            exit()
    elif dic is not None and DIC is None:
        if os.path.isfile(dic):
            return dic
        else:
            printf("Dictionary file not found", "error")
            exit()


def format_urls(url, URL):
    url_list = queue.Queue()

    if url and URL:
        printf("Parameter error, only one parameter of the same type can be set", "error")
        exit()
    elif url is None and URL is not None:
        if os.path.isfile(URL):
            try:
                with open(URL, encoding="utf-8") as f:
                    for line in f:
                        url_list.put(line.strip())
            except UnicodeDecodeError:
                printf("Encoding error, please convert the file to UTF-8", "error")
                exit()
        else:
            printf(URL + " does not exist!", "error")
            exit()
    elif url is not None and URL is None:
        url_list.put(url)

    return url_list


def format_batchs(single, mutile):
    temp_list = []

    if single and mutile:
        printf("Parameter error, only one parameter of the same type can be set", "error")
        exit()
    elif single == "" and mutile != "":
        if os.path.isfile(mutile):
            try:
                with open(mutile) as f:
                    for line in f:
                        temp_list.append(line.strip())
            except UnicodeDecodeError:
                printf("Encoding error, please convert the file to UTF-8", "error")
                exit()
        else:
            printf(mutile + " does not exist!", "error")
            exit()
    elif single != "" and mutile == "":
        temp_list.append(single)
    else:
        temp_list.append("")

    return temp_list


def format_nums(num):
    if num < 0:
        printf("You must set a postive number,already convert plus", "warning")
        return abs(num)
    else:
        return num


def read_file(file):
    if not file:
        return file
    else:
        with open(file, "r") as f:
            return f.read()
