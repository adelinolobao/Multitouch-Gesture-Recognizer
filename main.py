#!/usr/bin/env python
# encoding: utf-8
"""
File: main.py
Adelino Lobão
02/01/2012
"""

from pymt import *

"""
Class MTApplication
"""
class MTApplication(MTWidget):
	def __init__(self, **kwargs):
		super(MTApplication, self).__init__(**kwargs)
		self.gesture = [];
	
	#fired when a touch is down
	def on_touch_down(self, touch):
		touch.userdata['points'] = list(touch.pos)
		touch.userdata['trace'] = [touch.pos]
	
	#fired when a touch is moving
	def on_touch_move(self, touch):
		touch.userdata['points'].extend(touch.pos)
		touch.userdata['trace'].append(touch.pos)
	
	#fired when a touch is up
	def on_touch_up(self, touch):
		#build gesture
		self.gesture.append(touch.userdata['trace'])
		if len(getCurrentTouches()) == 0:
			print 'Recognition process...'
			#clean gesture
			self.gesture = []
	
	#draw widget
	def draw(self):
		set_color(1,1,1)
		for touch in getCurrentTouches():
			drawLine(touch.userdata['points'])

if __name__ == '__main__':
	window = MTWindow()
	app = MTApplication()
	window.add_widget(app)
	runTouchApp()