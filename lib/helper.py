#!/usr/bin/env python
# encoding: utf-8
"""
File: helper.py
Adelino Lobão
03/02/2012
"""

import sys
import os

"""
Class Helper
"""
class Helper:
	"""
	Function that returns the path where the template will be saved
	"""
	@staticmethod
	def returnTemplatePath():
		folderPath = ''
		#build the gesture folder path
		if(len(sys.argv) > 1):
			folderPath = './template/' + sys.argv[1]
		else:
			print 'Error gesture name'
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