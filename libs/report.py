# coding=utf-8

import os
import datetime

from .display import printf
from .config import *


def export_html(report_file, url, url_text):  # export result file
    try:  # open file
        report_f = open(report_file, "a+")  # use add method to open file
    except:
        printf("Cann't export the result!!!", "error")
        # set format to html
    export_web = "<ul><a href=\"{0}\" target=\"_blank\">{1}</a></ul>\n".format(
        url, url_text)
    report_f.write(export_web)
    report_f.close()


def init_html(filename):  # init the web form
    if os.path.exists("output"):
        pass
    else:
        try:
            os.mkdir("output")
        except:
            pass
    content_style = """
            a:link,
        :visited,
        :hover,
        :active {
            text-decoration: none;
            color: #000;
        }

        ul {
            list-style: circle;
        }

        .content {
            text-align: center;
            width: 80%;
            margin-top: 30px;
            border-radius: 10px;
            padding-top: 20px;
            padding-bottom: 20px;
            box-shadow: rgb(58, 58, 58) 10px 10px 30px 5px;
        }
    """
    head_html = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WMIN Report</title>
    <style type="text/css">
        %s
    </style>
</head>

<body>
    <center>
        <div class="content">
            <left>
                <h1>
                    <b>
                        WMIN V%s Scan Report
                    </b>
                </h1>
            </left>
            <h2>
                This report for <strong>[%s] at %s</strong>
            </h2>
            <hr>
            <!-- Content -->
""" % (content_style, version, filename, datetime.datetime.now())

    report_filename = "output/" + filename + ".html"  # set output filename
    try:
        report_file = open(report_filename, "w")  # use write to open file
    except:
        printf("result file can't be created!", "error")
    report_file.write(head_html)  # write to web form
    report_file.close()
    return report_filename  # return filename


def end_html(filename):

    foot_html = """
        </div>
    </center>

</body>

</html>"""
    with open(filename, "a+") as f:
        f.write(foot_html)
