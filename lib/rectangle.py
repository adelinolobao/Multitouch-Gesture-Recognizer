#!/usr/bin/env python
# encoding: utf-8
"""
File: rectangle.py
Adelino Lobão
01/02/2012
"""

"""
Class Rectangle
@param x - min position xx of rectangle
@param y - min position yy of rectangle
@param widht - rectangle width
@param height - rectangle height
"""
class Rectangle:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
	def x(self):
		return self.x
	
	def y(self):
		return self.y
		
	def width(self):
		return self.width
		
	def height(self):
		return self.height