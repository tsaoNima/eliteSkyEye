import sys
from Logging.structs import LogLevel
from Logging import log
from Constants import stringConstants
import setupTables

class SkyEyeDaemon(object):
	mLog = log.getLogInstance()

	def firstRunSetup(self):
		#Ask for the admin password to the DB. DO NOT STORE THIS.
		#Enter the db and do first time setup.
		pass

	def __init__(self, logPath=None):
		self.mLog = log.getLogInstance()
		#Open the log file!
		if logPath is None:
			logPath = stringConstants.kSkyEyeDefaultOutPath
		try:
			self.mLog.setLogFile(logPath)
		except:
			self.mLog.log(stringConstants.kFmtErrSkyEyeLogOpenFailed.format(logPath), LogLevel.Error)
		
		#Try to load settings.
		pass
		
		#Make sure DB is up. If not, try to start it.
		#	If we couldn't start DB, fail here. 
		
		#Is this our first boot?
		#	If so, enter setup.
		
		#Open server connection.
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
	outPath = stringConstants.kSkyEyeDefaultOutPath
	
	#Do startup.
	try:
		skyEye = SkyEyeDaemon(outPath)
	except:
		print stringConstants.kErrSkyEyeInitFailed
		print stringConstants.kFmtReason.format(sys.exc_info()[0])
		return
	
	#Now start listening for events.
	skyEye.run()
	
	#Do shutdown.
	skyEye.shutdown()

#This is the entry point for the application.
if __name__ == "__main__":
	main()