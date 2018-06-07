

def write_txt(res,path):
	import os
	f = open(path,"w+")
	for x in range(len(res)):
		f.write(str(res[x]) + "\n")
	f.close()
