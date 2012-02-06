#!/usr/bin/env python
# encoding: utf-8
"""
File: recognizer.py
Adelino Lobão
04/02/2012
"""

import math
from template import Template
from helper import Helper

"""
Constants
"""
halfDiagonal   = 0.5 * math.sqrt(250.0 * 250.0 + 250.0 * 250.0)
angleRange     = 45.0
anglePrecision = 2.0

"""
Class Recognizer
"""
class Recognizer:
	def __init__(self):
		self.templates = list()
		
	#recognize the gesture
	def recognize(self, traces):
		#security verification
		for trace in traces:
			if len(trace) < 2:
				return (None, 0)	#return none gesture
		#information about the gesture	
		numTracesGesture = len(traces)
		pointsGesture = Helper.normalizeGesture(traces)
		#comparison process
		bestDistance = float('infinity')
		bestTemplate = None
		for template in self.templates:
			distance = Helper.distanceAtBestAngle(pointsGesture, numTracesGesture, template, -angleRange, +angleRange, anglePrecision)
			if distance < bestDistance:
				bestDistance = distance
				bestTemplate = template
				score = 1.0 - (bestDistance / halfDiagonal)
		#get the best template
		if bestTemplate == None:
			return(None, 0)
		else:
			return (bestTemplate.name, score)
		
	#add a template
	def addTemplate(self, name, traces):
		template = Template(name, traces)
		self.templates.append(template)