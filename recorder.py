#!/usr/bin/env python
# encoding: utf-8
"""
File: recorder.py
Adelino Lobão
03/02/2012
"""

import sys
import os
import pickle
from pymt import *
from lib.window import WindowApp
from lib.helper import Helper

"""
Class RecorderWindowApp
"""
class RecorderWindowApp(WindowApp):
	def __init__(self, **kwargs):
		super(WindowApp, self).__init__(**kwargs)
		#store gesture
		self.gesture = []
	
	def on_touch_up(self, touch):
		self.gesture.append(touch.userdata['trace'])
		if len(getCurrentTouches()) == 0:
			templatePath = Helper.returnTemplatePath()
			output = open(templatePath, 'wb')
			pickle.dump(self.gesture, output)
			output.close()
			print templatePath + ' saved...'
			self.gesture = []

if __name__ == '__main__':
	window = MTWindow()
	app = RecorderWindowApp()
	window.add_widget(app)
	runTouchApp()