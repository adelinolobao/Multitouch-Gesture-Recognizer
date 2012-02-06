#!/usr/bin/env python
# encoding: utf-8
"""
File: template.py
Adelino Lobão
04/02/2012
"""

from point import Point
from helper import Helper

"""
Class Template
"""
class Template:
	def __init__(self, name, gesture):
		self.name = name
		self.numTracesGesture = len(gesture)
		self.points = Helper.normalizeGesture(gesture)