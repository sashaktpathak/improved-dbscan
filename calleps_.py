import os
eps = 3.0
str2 = "python dbscan2.py "
str3 =""
for i in range(500):
	st1 =  str(float(eps+float(i*1.0/20)))
	str3 = str2 + st1
	print(str3+"--")
	i += 5	
	os.system(str3)
	

