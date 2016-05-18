from sys import version_info

if version_info.major == 3:
    from printf.py3 import printf
else:
    from printf.py2 import printf

def export_result(export_file, web,web_text):  # export result file
    try:  # open file
        export_f = open(export_file, "a+") #use add to open file
        export_f.seek(274, 0)  # turn after to</center>
    except:
        printf("Cann't export the result!!!","error")
        # set format to html
    export_web = "<li><a href=\"{0}\">{1}</a></li>".format(web, web_text)
    export_web_len = len(export_web)
    export_f.write(export_web)
    export_f.seek(0, 0)  # goto file's head
    export_f.close()


def initialize_webframe(filename):  # init the web form
    web_frame = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
	<title>WMIN result</title>
	</head>
	<body>

	<center>
	<h1>
	<b>
	Website Miner
	</b>
	</h1>
	</center>

	</body>
</html>"""

    export_filename = filename + ".html"  # set output filename
    try:
        export_file = open(export_filename, "w")  # use write to open file
    except:
        printf("result file can't be created!","error")
    export_file.write(web_frame)  # write to web form
    export_file.close()
    return export_filename  # return filename
