#!/usr/bin/env python
# encoding: utf-8
"""
File: point.py
Adelino Lobão
02/01/2012
"""

"""
Class Point
@param x - coordinate xx
@param y - coordinate yy
"""
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return str(self.x) + ' ' + str(self.y)
	
	def x(self):
		return self.x
	
	def y(self):
		return self.y