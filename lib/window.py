#!/usr/bin/env python
# encoding: utf-8
"""
File: window.py
Adelino Lobão
03/02/2012
"""

from pymt import *

class WindowApp(MTWidget):
	def __init__(self, **kwargs):
		super(WindowApp, self).__init__(**kwargs)
		#store gesture
		self.gesture = []
	
	#fired when a touch is down
	def on_touch_down(self, touch):
		touch.userdata['points'] = list(touch.pos)
		touch.userdata['trace'] = [touch.pos]

	#fired when a touch is moving
	def on_touch_move(self, touch):
		touch.userdata['points'].extend(touch.pos)
		touch.userdata['trace'].append(touch.pos)

	#draw widget
	def draw(self):
		set_color(1,1,1)
		for touch in getCurrentTouches():
			drawLine(touch.userdata['points'])