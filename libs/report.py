# coding=utf-8

import os
import datetime

from .display import printf
from .config import *


def export_html(report_file, url, url_text):  # export result file
    try:  # open file
        report_f = open(report_file, "a+")  # use add method to open file
    except:
        printf("Can't export the result!", "error")
        # set format to html
    export_web = "<ul><a href=\"{0}\" target=\"_blank\">{1}</a></ul>\n".format(
        url, url_text)
    report_f.write(export_web)
    report_f.close()


def init_html(filename, version):
    output_dir = "output"
    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except OSError:
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
            width: 80%;
            margin-top: 30px;
            border-radius: 10px;
            padding-top: 20px;
            padding-bottom: 20px;
            box-shadow: rgb(58, 58, 58) 10px 10px 30px 5px;
        }
    """

    head_html = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WMIN Report</title>
    <style type="text/css">
        {content_style}
    </style>
</head>

<body>
    <center>
        <div class="content">
            <left>
                <h1>
                    <b>
                        WMIN V{version} Scan Report
                    </b>
                </h1>
            </left>
            <h2>
                This report is for <strong>[{filename}] at {datetime.datetime.now()}</strong>
            </h2>
            <hr>
            <!-- Content -->
"""

    report_filename = os.path.join(output_dir, filename + ".html")

    try:
        with open(report_filename, "w") as report_file:
            report_file.write(head_html)
    except IOError:
        print("Result file could not be created!")

    return report_filename


def end_html(filename):

    foot_html = """
        </div>
    </center>

</body>

</html>"""
    with open(filename, "a+") as f:
        f.write(foot_html)
