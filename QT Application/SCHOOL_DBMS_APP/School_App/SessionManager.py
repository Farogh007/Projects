
import os
import sys
import cv2

def imread(pathName, module=False):
	if not module:
		return cv2.imread(str(pathName))

def bgr2rgb(bgrImage):
	# Loading b g r components
	b,g,r = cv2.split(bgrImage)
	# Converting to RGB
	return cv2.merge([r,g,b])

class configuration():
	def __init__(self):	
		self.DATA_DIR = self.getPath2DATA()
		print(self.DATA_DIR)
		delimiter = "\\"
		self.DATA_PREFIX = self.DATA_DIR + delimiter

		self.INPUT_DIR = self.DATA_PREFIX + "INPUT"
		if not os.path.exists(self.INPUT_DIR):
			os.mkdir(self.INPUT_DIR)
		self.INPUT_PREFIX = self.INPUT_DIR + delimiter
		self.INPUT_PTR = 1110

		self.OUTPUT_DIR = self.DATA_PREFIX + "OUTPUT"
		if not os.path.exists(self.OUTPUT_DIR):
			os.mkdir(self.OUTPUT_DIR)
		self.OUTPUT_PREFIX = self.OUTPUT_DIR + delimiter
		self.OUTPUT_PTR = 1110
				
		self.EXTENSION = ".png"
		

	def getPtr_Input(self, input, last = True):
		'''
		if last == True: then get last pointer in folder
		if last == False: then get next pointer
		'''
		dir = ""
		input == "INPUT"
		dir = self.INPUT_DIR
		
			
		fileList = list()
		for item in os.listdir(dir):
			if item.split('.')[-1] == self.EXTENSION.split(".")[-1]:
				fileList.append(int(item.split('.')[0].split('_')[0]))
		fileList = sorted(fileList)
		
		pointer = 1110
		if (len(fileList)>0):
			pointer = (int)(fileList[-1])
		if last:
			return pointer
		return pointer+1

	def getPtr_Output(self, output, last = True):
		'''
		if last == True: then get last pointer in folder
		if last == False: then get next pointer
		'''
		dir = ""
		output == "OUTPUT"
		dir = self.OUTPUT_DIR
		
			
		fileList = list()
		for item in os.listdir(dir):
			if item.split('.')[-1] == self.EXTENSION.split(".")[-1]:
				fileList.append(int(item.split('.')[0].split('_')[0]))
		fileList = sorted(fileList)
		
		pointer = 1110
		if (len(fileList)>0):
			pointer = (int)(fileList[-1])
		if last:
			return pointer
		return pointer+1

	def refresh_Input(self, input):
		'''
		sets to next pointer by default
		'''
		
		input == "INPUT"
		self.INPUT_PTR = self.getPtr_Input(input, False)

	def refresh_Output(self, output):
		'''
		sets to next pointer by default
		'''
		
		output == "OUTPUT"
		self.OUTPUT_PTR = self.getPtr_Output(output, False)
		

	def imageFilename_Input(self, input):
		
		first = ""
		mid = ""
		
		if input == "INPUT":
			first = self.INPUT_PREFIX
			mid = str(self.INPUT_PTR)
	
		return first + mid + self.EXTENSION

	
	def imageFilename_Output(self, output):
		
		first = ""
		mid = ""
		
		if output == "OUTPUT":
			first = self.OUTPUT_PREFIX
			mid = str(self.OUTPUT_PTR)
	
		return first + mid + self.EXTENSION

	def getPath2DATA(self):
		dir=str(os.getcwd()).split('\\')[:-1]
		Path2DATA = ""
		for node in dir:
			Path2DATA += node + "\\"
		Path2DATA += "DATA"
		return Path2DATA

	def purgeAll_Input(self):
		
		try:
			print("Purging INPUT_DIR :" + INPUT_DIR)
			for item in os.listdir(self.INPUT_DIR):
				os.remove(item)
			os.removedirs(self.INPUT_DIR)
			print("Purge successful")
		except:
			print("Error occoured!")

	def purgeAll_Output(self):
		
		try:
			print("Purging OUTPUT_DIR :" + OUTPUT_DIR)
			for item in os.listdir(self.OUTPUT_DIR):
				os.remove(item)
			os.removedirs(self.OUTPUT_DIR)
			print("Purge successful")
		except:
			print("Error occoured!")
		
						
