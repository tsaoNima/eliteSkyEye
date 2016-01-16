import sys
from Output import log
from Constants import stringConstants
import setupTables

class SkyEyeDaemon(object):
	mLog = log.getLogInstance()

	def __init__(self, logPath=None):
		self.mLog = log.getLogInstance()	
		#Open the log file!
		if logPath is not None:
			self.mLog.setLogFile(stringConstants.kDefaultOutPath)
		
		#Open DB connection.
		pass
		
		#Make sure all the tables we need are actually there;
		#If not, ask if you want to generate defaults.
		setupTables.doSetupTables()
		
		#Establish connection to outputs (Discord, etc.)
		pass
	
		#Establish connection to inputs (HTTP API, etc.)
		#Report that we're open.
		pass
		
	def run(self):
		pass
		
	def shutdown(self):
		#Close any resources.
		self.mLog.shutdown()

def main():
	skyEye = None
	outPath = stringConstants.kDefaultOutPath
	
	#Do startup.
	try:
		skyEye = SkyEyeDaemon(outPath)
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