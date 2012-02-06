#!/usr/bin/env python
# encoding: utf-8
"""
File: helper.py
Adelino Lobão
03/02/2012
"""

import sys
import os
import pickle
import math
from point import Point
from rectangle import Rectangle

"""
Constants
"""
numPoints      = 64
squareSize     = 250.0
halfDiagonal   = 0.5 * math.sqrt(250.0 * 250.0 + 250.0 * 250.0)
angleRange     = 45.0
anglePrecision = 2.0
phi            = 0.5 * (-1.0 + math.sqrt(5.0)) # Golden Ratio

"""
Class Helper
Contains helper functions
"""
class Helper:

	#return the path where the template will be saved
	@staticmethod
	def returnTemplatePath():
		folderPath = ''
		#build the gesture folder path
		if(len(sys.argv) > 1):
			folderPath = './template/' + sys.argv[1]
		else:
			print '[Error] Gesture name'
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
	
		
	#return a dictionary with templates
	@staticmethod
	def returnTemplates():
		folderPath = './template/'
		if(os.path.exists(folderPath)):
			templates = {}	#dict that contains the gesture and templates
			for name in os.listdir(folderPath):	#iterate through folders
				if name == '.gitignore': #ignore this file
					continue
				templateList = list()
				gesturePath = folderPath + '/' + name
				if(os.path.isdir(gesturePath)):
					for template in os.listdir(gesturePath): #iterate through templates
						templatePath = gesturePath + '/' + template
						if(os.path.isfile(templatePath)):
							#load template
							tempFile = open(templatePath, 'rb')
							tempTemplate = pickle.load(tempFile)
							tempFile.close()		
							#append to the template list
							templateList.append(tempTemplate)
				#append to templates to the dictionary
				templates[name] = templateList
			if templates:
				return templates
			else:
				print '[Error] No templates'
				sys.exit()
		else:
			#create the gesture folder and terminate the program
			os.makedirs(folderPath)
			print '[Error] No templates'
			sys.exit()
		return
		
	#normalize the gesture received
	@staticmethod
	def normalizeGesture(gesture):
		resampledGesture = list()
		#resample traces of the gesture
		for trace in gesture:
			resampledTrace = [Point(point[0], point[1]) for point in trace]
			resampledTrace = Helper.resample(resampledTrace, numPoints)
			resampledGesture.append(resampledTrace)
		pointsGesture = list()
		#transform gesture in a list of points
		for trace in resampledGesture:
			for point in trace:
				pointsGesture.append(point)
		pointsGesture = Helper.rotateToZero(pointsGesture)
		pointsGesture = Helper.scaleToSquare(pointsGesture, squareSize)
		pointsGesture = Helper.translateToOrigin(pointsGesture)
		return pointsGesture
		
	#resample a set of points to a roughly equivalent, evenly-spaced set of points
	@staticmethod
	def resample(points, n):
		I = Helper.pathLength(points) / (n - 1) # interval length
		D = 0.0
		newpoints = [points[0]]
		i = 1
		while i < len(points) - 1:
			d = Helper.distance(points[i - 1], points[i])
			if (D + d) >= I:
				qx = points[i - 1].x + ((I - D) / d) * (points[i].x - points[i - 1].x)
				qy = points[i - 1].y + ((I - D) / d) * (points[i].y - points[i - 1].y)
				q = Point(qx, qy)
				newpoints.append(q)
				#insert 'q' at position i in points s.t. 'q' will be the next i
				points.insert(i, q)
				D = 0.0
			else:
				D += d
			i += 1

		#if we fall a rounding-error short of adding the last point, so add it if so
		if len(newpoints) == n - 1:
			newpoints.append(points[-1])
		return newpoints;
	
	#rotate a set of points such that the angle between the first point and center is 0
	@staticmethod	
	def rotateToZero(points):
		c = Helper.centroid(points)
		theta = math.atan2(c.y - points[0].y, c.x - points[0].x)
		return Helper.rotateBy(points, -theta)
		
	#rotate a set of points by a given angle
	@staticmethod
	def rotateBy(points, theta):
		c = Helper.centroid(points)
		cos = math.cos(theta)
		sin = math.sin(theta)
		newpoints = [];
		for point in points:
			qx = (point.x - c.x) * cos - (point.y - c.y) * sin + c.x
			qy = (point.x - c.x) * sin + (point.y - c.y) * cos + c.y
			newpoints.append(Point(qx, qy))
		return newpoints
	
	#scale a set of points to fit in a bounding box
	@staticmethod	
	def scaleToSquare(points, size):
		B = Helper.boundingBox(points)
		newpoints = []
		for point in points:
			qx = point.x * (size / B.width)
			qy = point.y * (size / B.height)
			newpoints.append(Point(qx, qy))
		return newpoints
	
	#translate a set of points, placing the centre point at the origin
	@staticmethod
	def translateToOrigin(points):
		c = Helper.centroid(points)
		newpoints = []
		for point in points:
			qx = point.x - c.x
			qy = point.y - c.y
			newpoints.append(Point(qx, qy))
		return newpoints;
		
	#best match between the gesture and the template
	@staticmethod
	def distanceAtBestAngle(points, numTracesGesture,T, a, b, threshold):
		if numTracesGesture != T.numTracesGesture:
			return float('inf')
		x1 = phi * a + (1.0 - phi) * b
		f1 = Helper.distanceAtAngle(points, T, x1)
		x2 = (1.0 - phi) * a + phi * b
		f2 = Helper.distanceAtAngle(points, T, x2)
		while abs(b - a) > threshold:
			if f1 < f2:
				b = x2
				x2 = x1
				f2 = f1
				x1 = phi * a + (1.0 - phi) * b
				f1 = Helper.distanceAtAngle(points, T, x1)
			else:
				a = x1
				x1 = x2
				f1 = f2
				x2 = (1.0 - phi) * a + phi * b
				f2 = Helper.distanceAtAngle(points, T, x2)
		return min(f1, f2)
	
	#returns the distance between a gesture and a template when rotated by theta
	@staticmethod
	def distanceAtAngle(points, T, theta):
		newpoints = Helper.rotateBy(points, theta)
		return Helper.pathDistance(newpoints, T.points)
			
	#returns the center of a geiven set of points
	@staticmethod	
	def centroid(points):
		x = 0.0
		y = 0.0
		for point in points:
			x += point.x
			y += point.y
		x /= len(points)
		y /= len(points)
		return Point(x, y)
	
	#returns a rectangle representing the bounding box that contains the points
	@staticmethod	
	def boundingBox(points):
		minX = float("+Infinity")
		maxX = float("-Infinity")
		minY = float("+Infinity")
		maxY = float("-Infinity")

		for point in points:
			if point.x < minX:
				minX = point.x
			if point.x > maxX:
				maxX = point.x
			if point.y < minY:
				minY = point.y
			if point.y > maxY:
				maxY = point.y
		return Rectangle(minX, minY, maxX - minX, maxY - minY)
		
	#distance between two paths
	@staticmethod
	def pathDistance(pts1, pts2):
		d = 0.0;
		for index in range(len(pts1)):
			if index >= len(pts2):
				return d / len(pts1)
			d += Helper.distance(pts1[index], pts2[index])
		return d / len(pts1)
	
	#length of the path represented by a set of points
	@staticmethod
	def pathLength(points):
		d = 0.0;
		for index in range(1, len(points)):
			d += Helper.distance(points[index - 1], points[index])
		return d
	
	#distance between two points
	@staticmethod
	def distance(p1, p2):
		dx = p2.x - p1.x
		dy = p2.y - p1.y
		return math.sqrt(dx * dx + dy * dy)