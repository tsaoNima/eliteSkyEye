'''
Created on Jan 15, 2016

@author: Me
'''

'''
Abstract class for objects that print output from the logger.
'''
class ListenerBase(object):
	def printMessage(self, message):
		raise NotImplementedError("Output modules must implement printMessage()!")
	
	def logLevel(self):
		raise NotImplementedError("Output modules must implement logLevel()!")
	
	def setLogLevel(self, pLogLevel):
		raise NotImplementedError("Output modules must implement setLogLevel()!")
	
	def tags(self):
		raise NotImplementedError("Output modules must implement tags()!")
	
	def addTag(self, pTag):
		raise NotImplementedError("Output modules must implement addTag()!")
	
	def removeTag(self, pTag):
		raise NotImplementedError("Output modules must implement removeTag()!")