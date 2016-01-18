'''
Created on Jan 15, 2016

@author: Me
'''
from structs import LogLevel

'''
Abstract class for objects that print output from the logger.
'''
class ListenerBase(object):
	mLogLevel = LogLevel.Info
	mTags = []
	
	def __init__(self):
		self.mLogLevel = LogLevel.Info
		self.mTags = []
	
	def printMessage(self, message):
		raise NotImplementedError("Listeners must implement printMessage()!")
	
	def logLevel(self):
		return self.mLogLevel
	
	def setLogLevel(self, pLogLevel):
		self.mLogLevel = pLogLevel
	
	def tags(self):
		return self.mTags
	
	def addTag(self, pTag):
		if pTag not in self.mTags:
			self.mTags.append(pTag)
	
	def removeTag(self, pTag):
		if pTag in self.mTags:
			self.mTags.remove(pTag)
	
	def clearTags(self):
		self.mTags = []