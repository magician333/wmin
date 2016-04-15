# coding : utf-8
from sys import argv,version_info
import scan
import os
help_doc = """ 
This is help document
\t-u(url) <target>\t\tset url
\t-d(dictionary) <target>\t\tset dictionary
\t-f(filename) <target>\t\tset output filename
\t-t(timeout) <target>\t\tset timeout\t*use float
\t-p(proxy) <target>\t\tset proxy\t*Example: ip:port~type
\t-m(max_code) <target>\t\tset maximum status code
\t-a(User-Agent) <target>\t\tset User-Agent
\t-i(ignore_text) <target>\t\tset ignore text
"""
result_file = ""
timeout = 0.4
proxy = None
ua = None
ignore_text = ""
url = ""
dictionary = ""
use_help = 0
U = False
D = False

if version_info.major == 3:
    from py3 import printf
else:
    from py2 import printf

if len(argv) <= 1:
    printf(help_doc)
else:
    argv.pop(0)  # delete the argv[0]
    for i in range(0, len(argv)):
        if "-u" == argv[i]:  # set url

            try:
                url = argv[i + 1]
                U = True
            except IndexError:
                printf("-u No argv!","error")

        elif "-d" == argv[i]:  # set dictionary
            try:

                dictionary = argv[i + 1]

                try:
                    open(dictionary)
                    D = True
                except FileNotFoundError:
                    printf(dictionary + " not found","error")
                    dictionary == None
                    break
                    
            except IndexError:
                printf("-d No argv!","error")

        elif "-f" == argv[i]:  # set output filename
            try:
                result_file = argv[i + 1]
            except IndexError:
                printf("-f No argv!","error")
        elif "-t" == argv[i]:  # set timeout

            try:

                try:
                    timeout = float(argv[i + 1])
                except ValueError:
                    printf("Must use postitive float,will use default","warning")

            except IndexError:
                printf("-t No argv!","error")

        elif "-p" == argv[i]:  # set proxy

            try:

                try:
                    if ":" and "~" in argv[i+1]:
                        proxy = dict({argv[i+1].split("~")[1]: argv[i+1].split(":")[0]+":"+argv[i+1].split("~")[0].split(":")[1]})
                        """
                        document:format:  IP:port~type
                        """
                    else:
                        raise IndexError

                except IndexError:
                    printf("Type Wrong !!!,will use default","warning")
                    proxy = None

            except IndexError:
                printf("-p No argv!","error")

        elif "-m" == argv[i]:  # set maximum status_code to show

            try:

                try:
                    max_code = argv[i + 1]
                except ValueError:
                    printf("Must use postitive integer,will use default","warning")

            except IndexError:
                 printf("-m No argv!","error")

        elif "-a" == argv[i]:	#set User-Agent

            try:
                ua = {"User-Agent":argv[i+1]}
            except IndexError:
                printf("-a No agrv!","error")

        elif "-i" == argv[i]:   #set ignore text

            try:
                ignore_text = argv[i+1]
            except IndexError:
                printf("-i No argv!","error")

        elif "-h" == argv[i]:
            printf(help_doc)

        elif 0 == len(argv):
            printf("Please enter the argv!","warning")

        else:

            if argv[i - 1] in ["-u", "-d", "-f", "-t", "-p","-a","-i","-m"]:
                pass
            else:
                printf("Can't find argv: " + argv[i],"warning")

    for para_test in argv:

        if argv.count(para_test)>1:
            printf("Have two same argv "+para_test,"error")
            U = False
            D = False

    if 0 == len(result_file):
        result_file == ""

    if U ==True and D == True:
        scan.dic_scan(url, dictionary, result_file, timeout, proxy,ua,ignore_text)
    elif U == True and D == False and dictionary == None:
        scan.get_info(url)
    else:
        pass
