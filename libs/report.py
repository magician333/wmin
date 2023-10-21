# coding=utf-8

import os
import datetime
import csv

from .display import printf
from .config import *


def export_html(filename, scanned_url):  # export result file
    # try:  # open file
    #     report_f = open(report_file, "a+")  # use add method to open file
    # except:
    #     printf("Can't export the result!", "error")
    #     # set format to html
    # export_web = "<ul><a href=\"{0}\" target=\"_blank\">{1}</a></ul>\n".format(
    #     url, url_text)
    # report_f.write(export_web)
    # report_f.close()

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
            list-style: none;
        }

        .content {
            width: 80%;
            margin-top: 30px;
            border-radius: 10px;
            padding-top: 20px;
            padding-bottom: 20px;
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
            <ul>
"""
    foot_html = """
    </ul>
        </div>
    </center>

</body>

</html>"""
    html_filename = os.path.join(output_dir, filename + ".html")
    with open(html_filename, "w", encoding="utf-8") as html_file:
        html_file.write(head_html)
        for i in scanned_url:
            html_file.write(
                "<li><a href=\"{0}\" target=\"_blank\">{0}\t\t\t{1}</a></li>\n".format(i[0], i[1]))
        html_file.write(foot_html)
    printf("The web report file has been saved \"./" +
           html_filename + "\"", "normal")


def export_csv(filename, scanned_url):
    output_dir = "output"
    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except OSError:
            pass

    csv_header = ["scanned_url", "status_code"]
    csv_filename = os.path.join(output_dir, filename + ".csv")
    with open(csv_filename, "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_header)
        for data in scanned_url:
            csv_writer.writerow(data)
    printf("The csv report file has been saved \"./" +
           csv_filename + "\"", "normal")
