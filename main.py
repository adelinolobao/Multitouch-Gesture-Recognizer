#!/usr/bin/env python
# encoding: utf-8
"""
File: main.py
Adelino Lobão
02/01/2012
"""

from pymt import *
from lib.window import WindowApp

"""
Class RecognizerWindowApp
"""
class RecognizerWindowApp(WindowApp):	
	def __init__(self, **kwargs):
		super(WindowApp, self).__init__(**kwargs)
		#store gesture
		self.gesture = []
	
	#fired when a touch is up
	def on_touch_up(self, touch):
		#build gesture
		self.gesture.append(touch.userdata['trace'])
		if len(getCurrentTouches()) == 0:
			print 'Recognition process...'
			#clean gesture
			self.gesture = []

if __name__ == '__main__':
	window = MTWindow()
	app = RecognizerWindowApp()
	window.add_widget(app)
	runTouchApp()