import sys
import os
import constants
import ruamel.yaml  # @UnresolvedImport
from Server import server
from Logging.structs import LogLevel
from Logging import log
from Exceptions import exceptions
from Logging import consoleListener

class SkyEyeDaemon(object):
	batchMode = False
	mLog = None
	server = None
	settings = None
	
	def loadSettings(self):
		settingsLoaded = False
		settingsYAML = None
		settingsPath = constants.kSkyEyeDefaultSettingsPath
		#Does the settings file exist?
		if os.path.isfile(settingsPath):
			#If so, try loading from disk.
			try:
				settingsFile = open(settingsPath, "r")
				settingsYAML = settingsFile.read()
				settingsFile.close()
				settingsLoaded = True
			except Exception as e:
				self.mLog.LogWarning(constants.kFmtErrSkyEyeSettingsOpenFailed.format(settingsPath) +
									"\n" +
									constants.kFmtReason.format(str(e)),
									constants.kTagSkyEye,
									constants.kMethodLoadSettings)
				settingsLoaded = False
		#If not (or loading failed)...
		if not settingsLoaded:
			#Load default settings.
			settingsYAML = constants.kDefaultSettings
			
		#Deserialize settings.
		self.settings = ruamel.yaml.load(settingsYAML, ruamel.yaml.RoundTripLoader)
	
	def saveSettings(self):
		"""Returns True if settings were saved to disk, False otherwise.
		"""
		
		assert self.settings is not None
		#Save settings to disk...
		settingsYAML = ruamel.yaml.dump(self.settings, Dumper=ruamel.yaml.RoundTripDumper)
		settingsPath = constants.kSkyEyeDefaultSettingsPath
		#If so, try loading from disk.
		try:
			settingsFile = open(settingsPath, "w")
			settingsFile.write(settingsYAML)
			settingsFile.close()
			return True
		except Exception as e:
			self.mLog.LogError(constants.kFmtErrSkyEyeSettingsSaveFailed.format(settingsPath) +
								"\n" +
								constants.kFmtReason.format(str(e)),
								constants.kTagSkyEye,
								constants.kMethodSaveSettings)
			return False
		pass
	
	def firstRunSetup(self):
		self.server.FirstTimeSetup()
		
		#Set up users...
		#Setup guest group role.
		#Guest can read tables, but not modify.
		#Setup base user group role.
		#Base users can see and update data.
		#Finally set up verifier group role.
		#Verifiers can confirm submitted data as valid.
		self.mLog.LogWarning("TODO: Client user setup not implemented!",
								constants.kTagSkyEye,
								constants.kMethodInit)
		pass
	
	#Init methods...
	def initFields(self, pBatchMode):
		self.batchMode = pBatchMode
		self.mLog = log.GetLogInstance()
		self.server = server.Server(self.batchMode)
		self.settings = None
	
	def initLog(self, logPath, logLevel):
		#Open the log file!
		if logPath is None:
			logPath = constants.kSkyEyeDefaultOutPath
		try:
			self.mLog.SetLogFile(logPath)
		except:
			self.mLog.LogError(constants.kFmtErrSkyEyeLogOpenFailed.format(logPath),
							constants.kTagSkyEye,
							constants.kMethodInit)
		#If we're not in batch mode, attach a listener so we can actually see what the crap's going on.
		if not self.batchMode:
			listener = consoleListener.ConsoleListener()
			listener.SetLogLevel(logLevel)
			self.mLog.Attach(listener)
			
	def verifyServer(self):
		problems = self.server.VerifyTables()
		#If not, ask if you want to generate defaults.
		if problems:
			self.mLog.LogWarning(constants.kWarnServerVerifyFailed,
								constants.kTagSkyEye,
								constants.kMethodInit)
			self.mLog.LogWarning("TODO: Table repair not implemented!",
								constants.kTagSkyEye,
								constants.kMethodInit)
			pass
	
	def initServer(self):
		"""Connects to server services, and initializes them as needed.
		Raises:
			* InternalServiceError if server login failed.
		"""
		#Is this our first boot?
		isFirstBoot = self.settings[constants.kSettingsFirstRun]
		if isFirstBoot:
			#If so, enter setup.
			self.initVerboseLog(constants.kInitFirstBoot)
			self.firstRunSetup()
		
		#Open server connection.
		self.initVerboseLog(constants.kInitServerLogin)
		if not self.server.Login():
			raise exceptions.InternalServiceError(constants.kErrLoginFailed) #TODO: add detail
		
		#Verify that tables match our expected schema.
		self.initVerboseLog(constants.kInitVerifyServer)
		self.verifyServer()
	
	def initIO(self):
		#Establish connection to outputs first.
		self.mLog.LogWarning("TODO: Output startup not implemented!",
								constants.kTagSkyEye,
								constants.kMethodInit)
		pass
	
		#Establish connection to inputs (HTTP API, etc.)
		self.mLog.LogWarning("TODO: Input startup not implemented!",
								constants.kTagSkyEye,
								constants.kMethodInit)
		pass
		
	#Shutdown methods...
	def shutdownIO(self):
		#Disconnect from INPUTS first.
		self.mLog.LogWarning("TODO: Input shutdown not implemented!",
								constants.kTagSkyEye,
								constants.kMethodShutdown)
		pass
	
		#Now disconnect from outputs.
		self.mLog.LogWarning("TODO: Output shutdown not implemented!",
								constants.kTagSkyEye,
								constants.kMethodShutdown)
		pass
		
	def initVerboseLog(self, message):
		self.mLog.LogVerbose(message, constants.kTagSkyEye, constants.kMethodInit)
	
	def shutdownVerboseLog(self, message):
		self.mLog.LogVerbose(message, constants.kTagSkyEye, constants.kMethodShutdown)
	
	def __init__(self, logPath=None, logLevel=LogLevel.Debug, pBatchMode=False):
		"""Class initializer.
		Raises:
			* InternalServiceError if server login failed.
		"""
		
		self.initFields(pBatchMode)
		self.initLog(logPath, logLevel)
		
		#Try to load settings.
		self.initVerboseLog(constants.kInitSettings)
		self.loadSettings()
		
		#Now get the server ready.
		self.initVerboseLog(constants.kInitServer)
		self.initServer()
		
		#Establish connections to input services (HTTP API, etc.)
		#and output services (Discord, etc.)
		self.initVerboseLog(constants.kInitIO)
		self.initIO()
		
		#Report that we're open.
		self.mLog.LogInfo(constants.kServerInitComplete,
						constants.kTagSkyEye,
						constants.kMethodInit)
		
	def Run(self):
		self.mLog.LogWarning("TODO: Run loop not implemented!",
								constants.kTagSkyEye,
								constants.kMethodRun)
		#Get input from sources.
		#Process that to RDA.
		#Once RDA timer up, merge to GDW.
		#Once GDW analysis tick up, perform GDW analysis.
		pass
		
	def Shutdown(self):
		#Notify users that the server is going down.
		self.mLog.LogInfo(constants.kServerShutdownStarted,
						constants.kTagSkyEye,
						constants.kMethodShutdown)
		
		#Disconnect from I/O services.
		self.shutdownVerboseLog(constants.kShutdownIO)
		self.shutdownIO()
		#Logout from the server.
		self.shutdownVerboseLog(constants.kShutdownServer)
		self.server.Logout()
		#Save out settings.
		self.shutdownVerboseLog(constants.kShutdownSettings)
		self.saveSettings()
		#Close any resources.
		self.mLog.Shutdown()

def main():
	"""Entry point for the daemon when run directly.
	"""
	
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

if __name__ == "__main__":
	main()