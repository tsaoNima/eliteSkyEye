import sys
from Output.outputBase import OutputBase
from structs import LogElem
from structs import LogLevel

sLogInstance = None
kLogBufferMaxLines = 1024
#All subscribers should print a message with this tag.
kTagAll = "*"
#This message is untagged.
kTagEmpty = ""

class Log(object):
	#Contains individual log elements.
	#Format is 
	logBuffer = []
	bufferHead = -1
	#Output modules that are interested in the log messages.
	subscribers = None
	#The file to write the log out to, if any.
	outFile = None
	
	'''
	Writes all entries in the buffer to the log file.
	'''
	def flushBuffer(self):
		#Do we have an output file?
		if self.outFile is not None:
			#If so, write all lines in the buffer to the file.
			for i in xrange(self.bufferHead + 1):
				msg = self.logBuffer[i]
				self.outFile.write(msg.message)
				self.outFile.write("\n")
		#Reset the buffer head.
		self.bufferHead = -1;
	
	def __init__(self, outPath=None):
		self.logBuffer = []
		#Preallocate buffer space because I don't want to use append() later.
		for i in xrange(kLogBufferMaxLines):
			emptyMsg = LogElem("", LogLevel.Verbose, kTagEmpty)
			self.logBuffer.append(emptyMsg)
		self.bufferHead = -1
		
		self.subscribers = []
		if outPath is not None:
			self.setLogFile(outPath)
		else:
			print "Log.__init__(): No log file specified, buffer will not be saved!"
	
	'''
	Closes all resources the log system may have been using.
	Should only be called at application shutdown.
	'''
	def shutdown(self):
		if self.outFile is not None:
			#Close the output file.
			self.outFile.close()
	
	'''
	Connects the given output module to the log buffer.
	'''
	def subscribe(self, subscriber):
		#Make sure the subscriber actually is an output module.
		if not issubclass(subscriber.__class__, OutputBase):
			print "Log.subscribe(): Can't attach subscriber {0}, subscriber doesn't derive from OutputBase!" % subscriber
			return
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
			#Does this subscriber care about this kind of message?
			if subscriber.logLevel() >= msg.logLevel and msg.tag in subscriber.tags():
				#If both are true, print the line to the subscriber.
				subscriber.printMessage(msg);
	
	'''
	Adds the requested message to the log's buffer
	and broadcasts the message to all interested subscribers.
	'''
	def log(self, message, level=LogLevel.Verbose, tag=kTagEmpty):
		#Add this line to the buffer:
		#Do we have space in the buffer?
		if self.bufferHead >= kLogBufferMaxLines-1:
			#If not, flush it first.
			self.flushBuffer()
		#Now add the line to the buffer.
		newMsg = LogElem(message, level, tag)
		self.bufferHead += 1
		self.logBuffer[self.bufferHead] = newMsg
		
		#Broadcast the new line to all subscribers.
		self.broadcast(newMsg)
	
	'''
	Gets the currently opened log file, if any.
	'''
	def logFile(self):
		if self.outFile is not None:
			return self.outFile.name
		else:
			return "(none)"
	
	'''
	Closes any currently open log file and uses the specified path as the new log file.
	If outPath is None or an empty string, does nothing.
	'''
	def setLogFile(self, outPath):
		newOutFile = None
		#Is the path valid?
		if outPath is not None or outPath != "":
			#Try to open the requested path; rollback if the open failed.
			print "setLogFile(): Opening log file {0}" % outPath
			try:
				newOutFile = open(outPath, 'a+')
			except:
				print "setLogFile(): Couldn't open \"{0}\", aborting!" % outPath
				print "Reason: {0}" % sys.exc_info()[0]
				return
		#Otherwise early out.
		else:
			print "setLogFile(): No log file specified, buffer will not be saved!"
			return
				
		#Close any log file we may have been using.
		if self.outFile is not None:
			print "setLogFile(): Closing log file {0}" % self.outFile.name
			self.outFile.close()
		
		#Now set the new output as our buffer's file.
		self.outFile = newOutFile
		print "setLogFile(): Switched to log file {0}" % newOutFile
		
'''
Gets an instance of Log representing the program's log buffer.
'''		
def getLogInstance():
	if sLogInstance is None:
		sLogInstance = Log()
	return sLogInstance
	