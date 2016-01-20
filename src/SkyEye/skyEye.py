import sys
import server
import constants
from Logging.structs import LogLevel
from Logging import log

class SkyEyeDaemon(object):
	batchMode = False
	mLog = None
	server = None
	
	def loadSettings(self):
		pass
	
	def firstRunSetup(self):
		#Ask for the admin password to the DB. DO NOT STORE THIS.
		#Enter the db and do first time setup.
		
		#Set up users...
		#Setup guest group role.
		#Guest can read tables, but not modify.
		#Setup base user group role.
		#Base users can see and update data.
		#Finally set up verifier group role.
		#Verifiers can confirm submitted data as valid.
		pass

	def __init__(self, logPath=None, pBatchMode=False):
		self.batchMode = pBatchMode
		self.mLog = log.GetLogInstance()
		self.server = server.Server(self.batchMode)
		#Open the log file!
		if logPath is None:
			logPath = constants.kSkyEyeDefaultOutPath
		try:
			self.mLog.SetLogFile(logPath)
		except:
			self.mLog.LogError(constants.kFmtErrSkyEyeLogOpenFailed.format(logPath), where="SkyEyeDaemon.__init__()")
		
		#Try to load settings.
		self.loadSettings()
		
		#Is this our first boot?
		isFirstBoot = pass
		if isFirstBoot:
			#If so, enter setup.
			self.firstRunSetup()
		
		#Open server connection.
		if not self.server.Login():
			raise RuntimeError("Couldn't login to server!") #TODO: add detail
		
		#Verify that tables match our expected schema.
		problems = self.server.VerifyTables()
		#If not, ask if you want to generate defaults.
		if problems:
			pass
		
		#Establish connection to outputs (Discord, etc.)
		pass
	
		#Establish connection to inputs (HTTP API, etc.)
		pass
		
		#Report that we're open.
		pass
		
	def Run(self):
		pass
		
	def Shutdown(self):
		#Disconnect from inputs.
		#Disconnect from outputs.
		#Logout from the server.
		self.server.Logout()
		#Close any resources.
		self.mLog.Shutdown()

def main():
	skyEye = None
	#TODO: switch these on console parameters.
	outPath = constants.kSkyEyeDefaultOutPath
	batchMode = False
	
	#Do startup.
	try:
		skyEye = SkyEyeDaemon(outPath, batchMode)
	except:
		print constants.kErrSkyEyeInitFailed
		print constants.kFmtReason.format(sys.exc_info()[0])
		return
	
	#Now start listening for events.
	skyEye.Run()
	
	#Do shutdown.
	skyEye.Shutdown()

#This is the entry point for the application.
if __name__ == "__main__":
	main()