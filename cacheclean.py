import os
folder = "cache"
for file in os.listdir(folder):
	file_path = os.path.join(folder, file)
	try:
		if os.path.isfile(file_path):
			os.unlink(file_path)
	except Exception, e:
		print e
