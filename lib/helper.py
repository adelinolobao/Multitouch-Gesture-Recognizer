#!/usr/bin/env python
# encoding: utf-8
"""
File: helper.py
Adelino Lobão
03/02/2012
"""

import sys
import os
import pickle

"""
Class Helper
"""
class Helper:

	#return the path where the template will be saved
	@staticmethod
	def returnTemplatePath():
		folderPath = ''
		#build the gesture folder path
		if(len(sys.argv) > 1):
			folderPath = './template/' + sys.argv[1]
		else:
			print '[Error] Gesture name'
			sys.exit()

		numTemplates = 0
		#calculate the number of templates inside the folder
		if(os.path.exists(folderPath)):
			#return the number of gesture templates
			numTemplates = len([name for name in os.listdir(folderPath) if os.path.isfile(folderPath + '/' +name)])
		else:
			#create the gesture folder
			os.makedirs(folderPath)
			
		numTemplates += 1
		#return the template path
		return folderPath + '/g' + str(numTemplates) + '.gesture'
	
		
	#return a dictionary with templates
	@staticmethod
	def returnTemplates():
		folderPath = './template/'
		if(os.path.exists(folderPath)):
			templates = {}	#dict that contains the gesture and templates
			for name in os.listdir(folderPath):	#iterate through folders
				if name == '.gitignore': #ignore this file
					continue
				templateList = list()
				gesturePath = folderPath + '/' + name
				if(os.path.isdir(gesturePath)):
					for template in os.listdir(gesturePath): #iterate through templates
						templatePath = gesturePath + '/' + template
						if(os.path.isfile(templatePath)):
							#load template
							tempFile = open(templatePath, 'rb')
							tempTemplate = pickle.load(tempFile)
							tempFile.close()		
							#append to the template list
							templateList.extend(tempTemplate)
				#append to templates to the dictionary
				templates[name] = templateList
			if templates:
				return templates
			else:
				print '[Error] No templates'
				sys.exit()
		else:
			#create the gesture folder and terminate the program
			os.makedirs(folderPath)
			print '[Error] No templates'
			sys.exit()
			
		return