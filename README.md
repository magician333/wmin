# wmin
Wmin介绍
-------

Wmin(Website Miner)是夜月魂信息安全团队-**紫火**使用纯Python开发的一款网站扫描器，中文名"网络矿工"



该软件使用命令行参数，详细参数如下(也可以使用-h命令):
------
-u(url) <target>
设置网址
-d(dictionary) <target>
设置字典
-f(filename) <target>
设置输出文件名称
-t(timeout) <target>
设置超时(注意:使用浮点数)
-p(proxy) <target>   
设置IP代理(格式: ip:port~type)
-m(max_code) <target>
设置最大状态码
-a(User-Agent) <target>
设置用户代理UA
-i(ignore_text) <target>
设置忽略页面包含的文本


其他小功能
------
*对于一个网站只指定了URL,Wmin将探测网站的IP地址和服务器类型
*Wmin使用彩色输出，建议在Linux/Unix下使用
*Wmin使用动态导入功能，Python2.x和Python3.x都可运行，但要求版本大于2.5
*Wmin依赖包：requests,colorama

如果bug反馈请发送邮件至[紫火](magician33333@163.com)
