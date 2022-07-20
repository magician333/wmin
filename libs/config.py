# coding=utf-8

#####################################################################################
### This file is used to configure the wmin default settings and basic parameters ###
#####################################################################################


###################################################################################
### Set wmin basic parameters, recommended that ordinary users do not modify it ###
###################################################################################

version = "0.3.2"
banner = """
                            ██              
                            ▀▀               | dev <%s> |
    ██      ██  ████▄██    ████     ██▄████ 
    ▀█  ██  █▀  ██ ██ ██     ██     ██▀   ██ 
     ██▄██▄██   ██ ██ ██     ██     ██    ██ 
     ▀██  ██▀   ██ ██ ██  ▄▄▄██▄▄▄  ██    ██ 
      ▀▀  ▀▀    ▀▀ ▀▀ ▀▀  ▀▀▀▀▀▀▀▀  ▀▀    ▀▀ """ % version
usage = "wmin.py -u url [options]"
description = '''
    Wmin is a web content discovery tool.
    It make requests and analyze the responses trying to figure out whether the
    resource is or not accessible.
    '''
epilog = "License, requests, etc: https://github.com/magician333/wmin"


###############################################################################################
### Set wmin default settings, you can modify the default settings to increase productivity ###
###############################################################################################

# Set default dictionary file, use dictionary filename(string)
default_dictionary = None

# Set default dictionary folder, use foldername(string)
default_Dictionaryfolder = None

# Set timeot Default 400ms
default_timeout = 0.4

# Set default user-agent
default_ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

# Set default ignoretext
default_ignoretext = ""

# Set default method
default_method = "get"

# Set default proxy
default_proxy = ""

# Set default proxy dict
default_Proxy = ""

# The url that sets the status code is not output to the report file,use numbers instead of characters
ignore_report_status_code = []

# The url that sets the status code is not displayed,use numbers instead of characters
ignore_display_status_code = []

# Set ssl,default False, if you need to use ssl, set it to the CA filename
default_ssl = False
