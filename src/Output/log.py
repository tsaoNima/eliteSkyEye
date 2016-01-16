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
			#Open the output file.
			try:
				self.outFile = open(outPath, 'w')
			except:
				print "Log.__init__(): Couldn't open \"{0}\"!" % outPath
				print "Reason: {0}" % sys.exc_info()[0]
				self.outFile = None
		else:
			print "Log.__init__(): No log file specified, buffer will not be saved!"
	
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
Gets an instance of Log representing the program's log buffer.
'''		
def getLogInstance():
	if sLogInstance is None:
		print "getLogInstance(): No log instance set up; did you call initLogInstance()?"
		assert False
	return sLogInstance

def initLogInstance(outPath=None):
	sLogInstance = Log(outPath)
	