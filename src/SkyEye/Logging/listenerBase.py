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
	
	def PrintMessage(self, message):
		raise NotImplementedError("Listeners must implement PrintMessage()!")
	
	def LogLevel(self):
		return self.mLogLevel
	
	def SetLogLevel(self, pLogLevel):
		self.mLogLevel = pLogLevel
	
	def Tags(self):
		return self.mTags
	
	def AddTag(self, pTag):
		if pTag not in self.mTags:
			self.mTags.append(pTag)
	
	def RemoveTag(self, pTag):
		if pTag in self.mTags:
			self.mTags.remove(pTag)
	
	def ClearTags(self):
		self.mTags = []