# coding=utf-8
import time
import queue
import requests
import socket

from . import report, config
from random import randint
from .display import printf, print_scanned_url
from urllib.parse import urlparse
from .config import *
from requests.packages import urllib3


class Net:
    """Url is the most important part of wmin,
    this class include the scan and get website information"""

    def __init__(self, domain, dictionary, timeout,
                 proxy, delay, ua, ignore_text, method, ssl):
        self.format_url(domain)
        self.dictionary = self.format_dict(dictionary)
        self.timeout = timeout
        self.proxy = list(map(self.set_proxy, proxy))
        self.ua = list(map(self.set_ua, ua))
        self.delay = delay
        self.ignore_text = ignore_text
        self.method = self.filter_method(method)
        self.fail_url = queue.Queue()
        self.ssl = ssl
        self.scanned_url = []  # format [(url,status_code)]

    def set_ua(self, ua):
        if "" == ua:
            return None
        else:
            return dict({"User-Agent": ua})

    def set_proxy(self, proxy):
        if proxy:
            if ":" in proxy and "@" in proxy:
                parts = proxy.split("@")
                proxy_type = parts[1]
                ip_port = parts[0]
                ip, port = ip_port.split(":")
                return {proxy_type: ip + ":" + port}
            else:
                printf("Wrong proxy format!", "warning")
        else:
            return None

    def set_reportfile(self):
        self.report_filename = report.init_html(self.hostname, config.version)

    def format_dict(self, dictionary):
        self.dict_line = queue.Queue()

        def process_line(line):
            if not line.startswith("#"):
                if line.startswith("/"):
                    self.dict_line.put(line.strip("\n"))
                else:
                    self.dict_line.put("/" + line.strip("\n"))

        def add_dictline(filename):
            try:
                with open(filename) as dic:
                    for line in dic.readlines():
                        process_line(line)
            except UnicodeDecodeError:
                printf("Coding error, please convert file to utf-8", "error")
                exit()
            except FileNotFoundError:
                self.dict_line = None

        if isinstance(dictionary, list):
            # dictionarys folder list
            for filename in dictionary:
                add_dictline(filename)
        else:
            # single dictionary file
            add_dictline(dictionary)

    def format_url(self, url):
        parsed_url = urlparse(url)
        protocol = parsed_url.scheme

        if not protocol:
            printf("Please enter URL with protocol", "warning")
            exit()

        purl = url.rstrip("/")
        hostname = parsed_url.netloc.rstrip("/")

        self.domain = purl
        self.hostname = hostname

    def filter_method(self, method):
        if method.lower() not in ["get", "post", "head"]:
            return None
        else:
            return method.lower()

    def scan(self):
        url = self.domain + self.dict_line.get_nowait()

        urllib3.disable_warnings()  # disable SSL verify warnings

        try:
            # Use the specified method
            kwargs = {
                "url": url,
                "timeout": self.timeout,
                "proxies": self.proxy[randint(0, len(self.proxy) - 1)],
                "headers": self.ua[randint(0, len(self.ua) - 1)],
                "verify": self.ssl,
                "allow_redirects": False
            }

            method_functions = {
                "get": requests.get,
                "post": requests.post,
                "head": requests.head
            }

            if self.method not in method_functions:
                printf("Invalid method specified: " + self.method, "error")
                exit()

            response = method_functions[self.method](**kwargs)

            code = response.status_code
            html = response.text

            if self.method == "head" and self.ignore_text != "":
                printf(
                    "Can't use head method and ignore text at the same time", "error")
                exit()

            if self.ignore_text != "" and self.ignore_text in html:
                return

            if code in ignore_display_status_code:
                return

            print_scanned_url(code, url)
            self.scanned_url.append((url, code))

            if code in ignore_report_status_code:
                return

        except KeyboardInterrupt:
            exit()
        except Exception:
            self.fail_url.put(url.replace(self.domain, ""))
            printf(url + "\tConnect error", "error")

    def get_info(self):
        printf("\n")
        printf("Domain:\t" + self.domain, "normal")

        try:
            response = requests.get(
                self.domain,
                timeout=self.timeout,
                proxies=self.proxy[randint(0, len(self.proxy) - 1)],
                headers=self.ua[randint(0, len(self.ua) - 1)],
                allow_redirects=False
            )

            try:
                server = response.headers["Server"]
                printf("Server:\t" + server, "normal")
            except KeyError:
                printf("Can't get server, Connect wrong", "error")

            try:
                ip = socket.gethostbyname(self.hostname)
                printf("IP:\t" + ip, "normal")
            except socket.gaierror:
                printf("Can't get IP, Connect wrong", "error")

            printf("")

        except KeyboardInterrupt:
            exit()
        except requests.exceptions.RequestException:
            printf("Failed to retrieve information for the domain", "error")

    def run(self):
        stime = time.time()

        top_prompt = "Total number of dictionary: " + \
            str(self.dict_line.qsize())
        printf("\n")
        printf(top_prompt, "normal")
        printf("")

        while not self.dict_line.empty():
            self.scan()

        while not self.fail_url.empty():
            reconnect_choice = input("Reconnect failed url? [Y/n]")
            if reconnect_choice.lower() in ["n", "no"]:
                break
            self.dict_line = self.fail_url
            self.fail_url = queue.Queue()
            while not self.dict_line.empty():
                self.scan()

        report.export_csv(self.hostname, self.scanned_url)
        report.export_html(self.hostname, self.scanned_url)

        bottom_prompt = "All work done! It took " + \
            str(time.time() - stime)[:5] + "s"
        printf("")
        printf(bottom_prompt, "normal")
