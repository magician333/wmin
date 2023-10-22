# coding=utf-8

import os
import datetime
import csv

from pathlib import Path
from .display import printf
from .config import *


class Report:
    def __init__(self, filename, scannd_url):
        self.filename = filename
        self.scanned_url = scannd_url

    def mkdir_project_dir(self):
        output_dir = "output"
        try:
            Path(output_dir).mkdir(exist_ok=True)

            index = 0
            self.project_file_dir = f"output/{self.filename}-{datetime.datetime.now().strftime('%Y-%m-%d')}-{index}"

            if os.path.exists(self.project_file_dir):
                project_dirs = next(os.walk('output'))[1]  # list output dir
                al_index_list = [int(dir.split("-")[-1]) for dir in project_dirs if self.filename +
                                 "-" + datetime.datetime.now().strftime("%Y-%m-%d") in dir]
                index = max(al_index_list) + 1 if al_index_list else 0

                self.project_file_dir = f"output/{self.filename}-{datetime.datetime.now().strftime('%Y-%m-%d')}-{index}"
            Path(self.project_file_dir).mkdir()

            self.html_filename, self.csv_filename = map(
                lambda ext: os.path.join(
                    self.project_file_dir, f"{self.filename}.{ext}"),
                ["html", "csv"]
            )
        except FileExistsError:
            printf("Can't mkdir output file!", "error")
        except PermissionError:
            printf("Can't mkdir project file!", "error")

    def export_file(self):
        self.mkdir_project_dir()
        printf("\n")
        printf(
            f"Report Files will save at \"{self.project_file_dir}\"", "normal")

        if self.export_html():
            printf(
                f"The web report file has been saved \"{self.html_filename}\"", "normal")
        else:
            printf("Failed to export web report file", "error")

        if self.export_csv():
            printf(
                f"The csv report file has been saved \"{self.csv_filename}\"", "normal")
        else:
            printf(f"Failed to export csv report file", "error")

    def export_html(self):  # export result file

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
                    This report is for <strong>[{self.filename}] at {datetime.datetime.now()}</strong>
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
        with open(self.html_filename, "w", encoding="utf-8-sig") as html_file:
            html_file.write(head_html)
            for i in self.scanned_url:
                html_file.write(
                    "<li><a href=\"{0}\" target=\"_blank\">{0}\t\t\t{1}</a></li>\n".format(i[0], i[1]))
            html_file.write(foot_html)
            return True

    def export_csv(self):
        csv_header = ["scanned_url", "status_code"]
        with open(self.csv_filename, "w", encoding="utf-8-sig", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csv_header)
            for data in self.scanned_url:
                csv_writer.writerow(data)
        return True
