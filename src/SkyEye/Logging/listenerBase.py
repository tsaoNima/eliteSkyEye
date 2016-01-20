'''
Created on Jan 15, 2016

@author: Me
'''
from structs import LogLevel

'''
Abstract class for objects that print output from the logger.
'''
class ListenerBase(object):
	def __init__(self):
		self.logLevel = LogLevel.Info
		self.tags = []
	
	def PrintMessage(self, message):
		raise NotImplementedError("Listeners must implement PrintMessage()!")
	
	def LogLevel(self):
		return self.logLevel
	
	def SetLogLevel(self, pLogLevel):
		self.logLevel = pLogLevel
	
	def Tags(self):
		return self.tags
	
	def AddTag(self, pTag):
		if pTag not in self.tags:
			self.tags.append(pTag)
	
	def RemoveTag(self, pTag):
		if pTag in self.tags:
			self.tags.remove(pTag)
	
	def ClearTags(self):
		self.tags = []