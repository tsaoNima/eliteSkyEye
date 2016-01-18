import sys
from listenerBase import ListenerBase
from structs import LogElem
from structs import LogLevel
import constants
from datetime import datetime
import pytz

sLogInstance = None

class Log(object):
	#Contains individual log elements.
	#Format is 
	logBuffer = []
	bufferHead = -1
	#Output modules that are interested in the log messages.
	subscribers = None
	#The file to write the log out to, if any.
	outFile = None
	
	def getTimeStamp(self):
		result = datetime.now(pytz.utc)
		return result
	
	#Writes all entries in the buffer to the log file.
	def flushBuffer(self):
		#Do we have an output file?
		if self.outFile is not None:
			#If so, write all lines in the buffer to the file.
			for i in xrange(self.bufferHead + 1):
				msg = self.logBuffer[i]
				self.outFile.write(constants.kLogFileLine.format(msg.dateTime, constants.kLogLevelNames[msg.logLevel], msg.tag, msg.message))
				self.outFile.write("\n")
		#Reset the buffer head.
		self.bufferHead = -1;
	
	#Prints the requested message
	#and also attempts to display it to listeners.
	def debugLog(self, message):
		print message
		self.logDebug(message)
	
	def __init__(self, outPath=None):
		self.logBuffer = []
		#Preallocate buffer space because I don't want to use append() later.
		for i in xrange(constants.kLogBufferMaxLines):
			emptyMsg = LogElem(self.getTimeStamp(), "", LogLevel.Verbose, constants.kTagEmpty)
			self.logBuffer.append(emptyMsg)
		self.bufferHead = -1
		
		self.subscribers = []
		self.debugLog(constants.kLogInitComplete)
		self.setLogFile(outPath)
	
	'''
	Closes all resources the log system may have been using.
	Should only be called at application shutdown.
	'''
	def shutdown(self):
		self.debugLog(constants.kLogInShutdown)
		#Flush the current buffer.
		self.flushBuffer()
		
		#Unhook all subscribers.
		for s in self.subscribers:
			self.subscribers.remove(s)
		
		#Close the output file.
		if self.outFile is not None:
			self.outFile.close()
	
	'''
	Connects the given output module to the log buffer.
	Raises:
		* TypeError if [subscriber] is not a subclass of ListenerBase.
	'''
	def subscribe(self, subscriber):
		#Make sure the subscriber actually is an output module.
		if not issubclass(subscriber.__class__, ListenerBase):
			failStr = constants.kFmtLogSubscribeFailed.format(subscriber)
			raise TypeError(failStr)
		#Otherwise, add it to the subscriber list.
		self.subscribers.append(subscriber)
	
	'''
	Broadcasts the current line to all subscribers.
	'''
	def broadcast(self, msg):
		assert self.bufferHead >= 0
		
		#For each subscriber:
		for subscriber in self.subscribers:
			#Does this subscriber have a high enough verbosity?
			levelMatches = msg.logLevel >= subscriber.logLevel()
			#Does this subscriber care about this kind of message?
			tagMatches = (msg.tag == constants.kTagAll or 
						not subscriber.tags() or
						msg.tag in subscriber.tags())
			if levelMatches and tagMatches:
				#If both are true, print the line to the subscriber.
				subscriber.printMessage(msg);
	
	'''
	Adds the requested message to the log's buffer
	and broadcasts the message to all interested subscribers.
	'''
	def log(self, message, level=LogLevel.Verbose, tag=constants.kTagEmpty):
		#Add this line to the buffer:
		#Do we have space in the buffer?
		if self.bufferHead >= constants.kLogBufferMaxLines-1:
			#If not, flush it first.
			self.flushBuffer()
		#Now add the line to the buffer.
		newMsg = LogElem(self.getTimeStamp(), message, level, tag)
		self.bufferHead += 1
		self.logBuffer[self.bufferHead] = newMsg
		
		#Broadcast the new line to all subscribers.
		self.broadcast(newMsg)
		
	def logVerbose(self, message, tag=constants.kTagEmpty):
		self.log(message, LogLevel.Verbose, tag)
	
	def logDebug(self, message, tag=constants.kTagEmpty):
		self.log(message, LogLevel.Debug, tag)
	
	def logInfo(self, message, tag=constants.kTagEmpty):
		self.log(message, LogLevel.Info, tag)
	
	def logWarning(self, message, tag=constants.kTagEmpty):
		self.log(message, LogLevel.Warning, tag)
		
	def logError(self, message, tag=constants.kTagEmpty):
		self.log(message, LogLevel.Error, tag)
	
	'''
	Gets the currently opened log file, if any.
	'''
	def logFile(self):
		if self.outFile is not None:
			return self.outFile.name
		else:
			return constants.kStrNone
	
	'''
	Closes any currently open log file and uses the specified path as the new log file.
	If outPath is None or an empty string, does nothing.
	'''
	def setLogFile(self, outPath):
		newOutFile = None
		#Early out.
		if outPath is None or not outPath:
			self.debugLog(constants.kLogNoFileOpen)
			return
		
		#Is the path valid?
		#Try to open the requested path; rollback if the open failed.
		print constants.kFmtLogOpeningLogFile.format(outPath)
		try:
			newOutFile = open(outPath, constants.kLogFileMode)
		except:
			self.debugLog(constants.kFmtLogFileOpenFailed.format(outPath, sys.exc_info()[0]))
			return
				
		#Close any log file we may have been using.
		if self.outFile is not None:
			self.debugLog(constants.kFmtLogClosingLogFile.format(self.outFile.name))
			self.outFile.close()
		
		#Now set the new output as our buffer's file.
		self.outFile = newOutFile
		self.debugLog(constants.kFmtLogSwitchedLogFile.format(newOutFile.name))
		
'''
Gets an instance of Log representing the program's log buffer.
'''		
def getLogInstance():
	global sLogInstance
	if sLogInstance is None:
		sLogInstance = Log()
	return sLogInstance
	