# wmin
Wmin介绍
-------

Wmin(Website Miner)是夜月魂信息安全团队-**紫火**和**10087**使用纯Python开发的一款网站扫描器，中文名"网络矿工"



该软件使用命令行参数，详细参数如下(也可以使用-h命令):
------
-u(url) <target>
设置网址

-U(urls) <target>
设置批量处理url

-d(dictionary) <target>
设置字典

-D(dictionarys) <target>
设置多字典目录

-r(report_filename) <target>
设置输出报告文件名

-t(timeout) <target>
设置超时(单位:秒)

-p(proxy) <target>
设置IP代理(格式: ip:port@type)

-P(Proxy file) <target>
设置IP代理文件路径

-m(method) <target>
设置请求方式

-e(delay) <target>
设置延迟(单位:秒)

-a(User-Agent) <target>
设置UA

-A(User-Agent file)
设置UA文件

-i(ignore_text) <target>
设置忽略页面包含的文本



说明
------
* 如果不指定扫描报告结果文件名,文件名则默认为网站url
* 扫描报告一律生成在output文件夹下
* 相同功能的大小写参数不能同时进行
* 多url文件要求每个url占一行,必须是文本文件
* 如果使用了批量url扫描则不能设置结果输出文件名
* 多字典要求指定一个字典目录,目录下必须放置文本字典文件
* 字典文件和多url批量处理文件的编码都必须是utf-8
* 扫描目录的请求方式支持get,post,head


其他
------
* 对于一个网站只指定了URL,Wmin将探测网站的IP地址和服务器类型

* Wmin使用动态导入功能，Python2.x和Python3.x都可运行，但要求Python版本大于2.5，但请您尽快使用Python3,未来本程序也将对Python2.x不再支持

* Wmin依赖包：requests,colorama (本程序已经自带)

如果bug反馈请发送邮件至magician33333@163.com
