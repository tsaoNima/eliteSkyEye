import sys
from Output import log
from Constants import stringConstants

class SkyEyeDaemon(object):
	mLog = log.getLogInstance()

	def __init__(self):
		self.mLog = log.getLogInstance()	

	def startup(self, logPath=None):
		#Open the log file!
		if logPath is not None:
			self.mLog.setLogFile(stringConstants.kDefaultOutPath)
		
		#Open DB connection.
		#Make sure all the tables we need are actually there;
		#If not, ask if you want to generate defaults.
		
		
		#Establish connection to outputs (Discord, etc.)
		
		#Establish connection to inputs (HTTP API, etc.)
		#Report that we're open.
		
	def run(self):
		pass
		
	def shutdown(self):
		#Close any resources.
		self.mLog.shutdown()

def main():
	skyEye = SkyEyeDaemon()
	
	#Do startup.
	try:
		skyEye.startup()
	except:
		print stringConstants.kErrSkyEyeInitFailed
		print stringConstants.kFmtReason % sys.exc_info()[0]
		return
	
	#Now start listening for events.
	skyEye.run()
	
	#Do shutdown.
	skyEye.shutdown()

#This is the entry point for the application.
if __name__ == "__main__":
	main()