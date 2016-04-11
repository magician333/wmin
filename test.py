def test(f):
	web="http://loaclhost"
	line = f.readline()                                              
	while line:  # 逐行读取
		line = line.strip('\n')  # 去除换行                      
		if line.startswith("/"):
			web = web + line
			print(web)
		else:                                            
			web = web + "/" + line
			print(web)



print(test(open("dic.txt")))
