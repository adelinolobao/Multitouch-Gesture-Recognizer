#!/usr/bin/env python
# encoding: utf-8
"""
File: recognizer.py
Adelino Lobão
04/02/2012
"""

from template import Template

"""
Class Recognizer
"""
class Recognizer:
	def __init__(self):
		self.templates = list()
		
	#add a template
	def addTemplate(self, name, traces):
		template = Template(name, traces)
		self.templates.append(template)