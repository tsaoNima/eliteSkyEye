'''
Created on Jan 15, 2016

@author: Me
'''
import constants
from listenerBase import ListenerBase
from structs import LogLevel
import colorama
from colorama.ansi import Style

#Specifies what color a line should be based on its verbosity.
sFormatMap = {
			LogLevel.Verbose : colorama.Fore.CYAN,
			LogLevel.Debug : colorama.Fore.GREEN,
			LogLevel.Info : colorama.Fore.WHITE,
			LogLevel.Warning : colorama.Fore.YELLOW,
			LogLevel.Error : colorama.Fore.RED
			}

'''
Prints log info to standard output.
'''
class ConsoleListener(ListenerBase):
	mLogLevel = LogLevel.Info
	mTags = []
	
	def __init__(self, pLogLevel=LogLevel.Info, pTags=[""]):
		self.mLogLevel = pLogLevel
		self.mTags = pTags
		#Start Colorama.
		colorama.init()
		
	def shutdown(self):
		#Shutdown Colorama.
		colorama.deinit()
		
	def printMessage(self, message):
		#Color depends on severity.
		textColor = sFormatMap[message.logLevel] + Style.BRIGHT
		#Print the message and then print a newline.
		print textColor + constants.kStdOutLine.format(message.dateTime, message.tag, message.message) + Style.RESET_ALL
	
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