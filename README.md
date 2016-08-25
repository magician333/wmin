# wmin
Wmin介绍
-------
![logo](https://magician333.github.io/logo.png)
Wmin(Website Miner)是夜月魂信息技术团队-**紫火**和**10087**使用纯Python开发的一款网站目录扫描器，中文名"网络矿工"


该软件使用命令行参数，详细参数如下:
------
* -u(url) **target**    设置网址
* -U(url file) **target**    设置批量处理url
* -d(dictionary) **target**    设置字典
* -D(dictionary folder) **target**    设置多字典目录
* -t(timeout) **target**    设置超时(单位:秒)
* -p(proxy) **target**    设置IP代理(格式: ip:port@type)
* -P(Proxy file) **target**    设置IP代理文件路径
* -m(method) **target**    设置请求方式
* -e(delay) **target**    设置延迟(单位:秒)
* -a(User-Agent) **target**    设置UA
*  -A(User-Agent file) **target**    设置UA文件
* -i(ignore_text)    **target**    设置忽略页面包含的文本

界面展示
------
![scan](https://magician333.github.io/scan.png)
***
![get_info](https://magician333.github.io/get_info.png)
***
![help](https://magician333.github.io/help.png)

特点
------
* 支持多url、多字典批量处理
* 支持自定义代理
* 支持自定义UA
* 支持忽略文本
* 支持多请求方式
* 支持随机UA，随机代理切换
* 支持网站基本信息获取
* 支持延时扫描
* 支持Linux、BSD、Mac、Windows、Android([Termux](https://termux.com))多平台

说明
------
* 扫描报告一律生成在output文件夹下，文件名为网站url
* 相同功能的大小写参数不能同时进行
* 批量处理文件要求每个url占一行，必须是文本文件
* 多字典要求指定一个字典目录,目录下必须放置文本字典文件
* 只指定网站url，将获取网站的IP地址和服务器类型
* 批量处理文件的编码必须是utf-8
* 扫描方式支持get、post、head

规划
------
* 多线程/多协程/多进程扫描
* 分布式扫描
* 多种类扫描报告

问题
-----
* 暂无

其他
------
* Wmin使用动态导入功能，Python2.x和Python3.x都可运行，但要求Python版本大于2.5，但请您尽快使用Python3,未来本程序也将对Python2.x不再支持

* Wmin第三方依赖库：requests、colorama (程序内部已集成)
