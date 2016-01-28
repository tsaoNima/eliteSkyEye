'''
Created on Jan 18, 2016

@author: Me
'''
import constants
import psycopg2
from .. import genericStrings
from ..Keychain import constants as KeychainConstants
from ..Database.database import Database
from ..Logging import log
from ..Keychain import keychainOps
from ..Logging.structs import LogLevel
from ..Exceptions import exceptions
from Subsystems.GeoWarehouse.geoWarehouse import GeoWarehouse
from Subsystems.ReconAnalyzer.reconAnalyzer import ReconAnalyzer
from SkyEye.Exceptions.exceptions import PasswordInvalidError

sLog = log.GetLogInstance()

class Server(object):
	"""Represents the server connection.
	"""
		
	def __init__(self):
		self._userName = constants.kServerDBAdminName
		self.subsystems = []
		#Database connections for subsystems.
		self.subsystems.append(GeoWarehouse())
		self.subsystems.append(ReconAnalyzer())
		#If true, server should not accept standard input.
		self._batchMode = True
		#If true, server is connected to all internal services.
		self._loggedIn = False
	
	@property
	def UserName(self):
		"""Returns the username used to access the server.
		"""
		return self._userName
	
	@UserName.setter
	def UserName(self, val):
		"""Sets the username used to access the server.
		"""
		
		#Sanity check.
		if val is None or not val:
			self._userName = constants.kServerDBAdminName
		else:
			self._userName = val  
	
	@property
	def LoggedIn(self):
		"""Returns whether or not the server is connected to its databases.
		"""
		return self._loggedIn
	
	@property
	def BatchMode(self):
		"""Returns whether or not the server is running in batch mode.
		"""
		return self._batchMode
	
	@BatchMode.setter
	def BatchMode(self, val):
		"""Sets whether or not we are in batch mode.
		Raises:
			* WrongModeError if called while self.LoggedIn is True.
		"""
		
		if self.LoggedIn:
			raise exceptions.WrongModeError("Attempted to set server batch mode while connected to the server!")
		else:	
			self._batchMode = bool(val)
	
	def getPassword(self):
		"""Gets the password for the server admin.
		Returns: The password for the server admin if it is set, None otherwise.
		"""
		return keychainOps.GetPassword(KeychainConstants.kServiceDatabase)
	
	def haveCredentials(self):
		"""Returns True if the server admin password is set, False otherwise.
		"""
		
		return self.getPassword() is not None
	
	def requestNewCredentials(self):
		"""Returns True if given new credentials, returns False otherwise.
		Raises: WrongModeError if we are in batch mode, since we can't get a new password without user input.
		"""
		
		#Are we in batch mode?
		if self.BatchMode:
			#Throw an exception!
			raise exceptions.WrongModeError(genericStrings.kErrCannotPerformInBatchMode)
			return False	
		#Otherwise, ask for new login info.
		try:
			newPass = keychainOps.PromptPassword(constants.kFmtPromptNewDBPassword.format(self.UserName))
			#Confirm the password.
			confirmPass = keychainOps.PromptPassword(constants.kFmtConfirmNewDBPassword.format(self.UserName))
			numFails = 0
			while confirmPass != newPass:
				if numFails >= constants.kMaxNumPrompts:
					sLog.LogError(constants.kErrTooManyPromptsFailed,
								constants.kTagServer,
								constants.kMethodRequestNewCredentials)
					return False
				numFails += 1
				confirmPass = keychainOps.PromptPassword(constants.kErrNewDBPasswordMismatch)
			keychainOps.SetPassword(KeychainConstants.kServiceDatabase, newPass)
			return True
		except exceptions.SkyEyeError as e:
			sLog.LogError(genericStrings.kFmtUnhandledError.format(e) +
						"\n" + constants.kErrNewCredentialsFailed,
						constants.kTagServer,
						constants.kMethodRequestNewCredentials)
			return False
	
	def canLogin(self, pPassword):
		"""Returns True if we can log into the database with the given user/password pair,
		False otherwise.
		Raises: psycopg2.Error if anything besides an invalid password error occurs.
		"""
		try:
			tempConnect = Database()
			tempConnect.Connect(constants.kSysAdminDatabaseName, self.UserName, pPassword)
			tempConnect.Disconnect()
			return True
		except exceptions.PasswordInvalidError:
			#If this was a password failure, we're fine.
			return False
		#Otherwise we need to abort.
		except exceptions.SkyEyeError as e:
			raise e
	
	def promptCredentials(self):
		"""Returns True if we have or were able to get valid credentials,
		returns False otherwise.
		"""
		
		#First, see if we have valid credentials.
		#Do we have any credentials?
		if self.haveCredentials():
			#If so, try logging in.
			password = self.getPassword()
			try:
				#If those credentials worked, quit here.
				if self.canLogin(password):
					return True
			except psycopg2.Error as e:
				#If a connection error occured, abort now.
				sLog.LogError(genericStrings.kFmtUnhandledError.format(e),
							constants.kTagServer,
							constants.kMethodGetCredentials)
				return False
	
		#If we don't have credentials or the credentials don't work,
		#enter new credentials loop (max 3 tries):
		#Abort at this step if we're in batch mode.
		if self.BatchMode:
			sLog.LogError(genericStrings.kErrCannotPerformInBatchMode,
						constants.kTagServer,
						constants.kMethodGetCredentials)
			return False
		else:
			for i in xrange(constants.kMaxNumPrompts):  # @UnusedVariable
				#Request new credentials.
				if not self.requestNewCredentials():
					sLog.LogError(constants.kErrCredentialRequestFailed,
								constants.kTagServer,
								constants.kMethodGetCredentials)
					return False
				#If the credentials work, exit loop.
				if self.canLogin(self.getPassword()):
					return True
	
		#Do we still not have a valid login?
		#Report that login attempts have been exceeded.
		sLog.LogError(constants.kErrTooManyPromptsFailed, constants.kTagServer, constants.kMethodGetCredentials)
		return False
	
	def setupLog(self, message, logLevel):
		sLog.Log(message, logLevel, constants.kTagServer, constants.kMethodFirstTimeSetup)
		print message
	
	def dropEverything(self, sysAdminDB):
		"""
		Drops all data and users!
		Raises:
			* InternalServiceError if any data was not successfully dropped.
		"""
		#Drop all databases.
		for subsystem in self.subsystems:
			if not sysAdminDB.DropDatabase(subsystem.Name):
				raise exceptions.InternalServiceError("Failed to drop database {0}!".format(subsystem.Name))
		#Drop all users now.
		if not sysAdminDB.DropUser(self.UserName):
			raise exceptions.InternalServiceError("Failed to drop user {0}!".format(self.UserName))
	
	def createDBAdmin(self, sysAdminDB):
		"""Creates self.UserName as the server's administrator user.
		Raises:
			* InternalServiceError if the database administrator account couldn't be created.
		"""
		#Create our DB admin. Ask for DB admin password
		#and store it in the keychain.
		self.setupLog(constants.kFirstTimeSetupCreatingDBAdmin, LogLevel.Debug)
		credentialsReset = False
		while not credentialsReset:
			credentialsReset = self.requestNewCredentials()
			
		#Perform the CREATE USER query. This is the DB admin,
		#so it should have rights to create a database.
		if not sysAdminDB.CreateUser(self.UserName,
									self.getPassword(),
									canCreateDB=True):
			raise exceptions.InternalServiceError("Failed to create user {0}!".format(self.UserName))
		self.setupLog(constants.kFirstTimeSetupDBAdminCreated, LogLevel.Debug)
	
	def ClearCredentials(self):
		"""Deletes any existing password for the current user from the server's keychain!
		"""
		sLog.LogWarning(constants.kFmtWarnClearingCredentials.format(self.UserName),
					constants.kTagServer, constants.kMethodClearCredentials)
		if self.haveCredentials():
			keychainOps.DeletePassword(KeychainConstants.kServiceDatabase)
	
	def Login(self):
		"""Logs the user in.
		Raises:
			* PasswordMissingError if we couldn't get login credentials.
			* InvalidPasswordError if the given password was somehow invalid.
			* InternalServerError if a subsystem failed to start.
		"""
		
		sLog.LogInfo(constants.kFmtLoginStarted.format(self.UserName),
					constants.kTagServer,
					constants.kMethodLogin)
		
		#If we absolutely couldn't get credentials, abort.
		if not self.promptCredentials():
			raise exceptions.PasswordMissingError(self.UserName)
		
		#Otherwise, connect to the databases with the credentials we got.
		user = self.UserName
		password = self.getPassword()
		startedSubsystems = []
		for subsystem in self.subsystems:
			try:
				subsystem.Start(user, password)
				startedSubsystems.append(subsystem)
			except exceptions.SkyEyeError as e:
				#If anything goes wrong, mark that we're not logged in.
				self._loggedIn = False
				#Shutdown all started subsystems.
				for readySubsystem in startedSubsystems[::-1]:
					readySubsystem.Shutdown()
				#Bubble up the exception.
				raise e
			
		self._loggedIn = True
		
		#Report if all subsystems could be connected.
		sLog.LogInfo(constants.kFmtLoginComplete.format(self.UserName),
					constants.kTagServer,
					constants.kMethodLogin)
	
	def Logout(self):
		"""Disconnects from the server.
		"""
		
		#Disconnect from subsystems in reverse order.
		for subsystem in self.subsystems[::-1]:
			subsystem.Shutdown()
			
		self._loggedIn = False
		#Report that we're logged out.
		sLog.LogInfo(constants.kFmtLogoutComplete.format(self.UserName), constants.kTagServer, constants.kMethodLogout)
	
	def VerifyDatabases(self):
		"""Checks that all tables in the server match expected schema.
		Returns: A list of any verification problems with the server's subsystems.
		Raises:
			* WrongModeError if we're not actually logged into the server.
		"""
		#Abort if we're not logged in.
		if not self.LoggedIn:
			raise exceptions.WrongModeError(constants.kErrNotLoggedIn)
		
		#Perform verification.
		results = []
		for subsystem in self.subsystems:
			subsystemResults = subsystem.Verify()
			if subsystemResults:
				results.append(subsystemResults)
				
		return results
		
	def FirstTimeSetup(self):
		"""Creates database admin account and subsystem databases for the first run.
		This can drop all existing data; back up any existing data before running this.
		Raises:
			* WrongModeError if server is in batch mode.
			* InternalServiceError if the server databases couldn't be connected to.
		"""
		
		#If we're in batch mode, quit now.
		if self.BatchMode:
			raise exceptions.WrongModeError(genericStrings.kErrCannotPerformInBatchMode)
		
		self.setupLog(constants.kFirstTimeSetupStarting, LogLevel.Info)
		self.setupLog(constants.kFirstTimeSetupWarnDataLoss, LogLevel.Warning)
		
		#Login loop:
		sysAdminDB = Database()
		sysAdminPW = ""
		sysAdminPWValid = False
		while not sysAdminPWValid:
			#Ask for the system admin password to the DB.
			sysAdminPW = keychainOps.PromptPassword(constants.kFirstTimeSetupPromptSysAdminPassword)
			#Logon to "postgres" as the admin "postgres".
			try:
				sysAdminDB.Connect(constants.kSysAdminDatabaseName,
							constants.kSysAdminUserName,
							sysAdminPW)
				sysAdminPWValid = True
			except exceptions.PasswordInvalidError:
				print constants.kFirstTimeSetupErrSysAdminPasswordInvalid
				sysAdminPWValid = False
			#Bubble any other exception up.
			except exceptions.SkyEyeError as e:
				raise e
				
		#Clear all existing data.
		self.dropEverything(sysAdminDB)
		self.createDBAdmin(sysAdminDB)
		dbAdminPW = self.getPassword()
		
		#Logout from server admin!
		sysAdminDB.Disconnect()
		
		#Now iterate over each subsystem...
		for subsystem in self.subsystems:
			#Create the database and set up default tables.
			subsystem.CreateAndSetup(self.UserName, dbAdminPW)
	
		#We're done!
		self.setupLog(constants.kFirstTimeSetupComplete, LogLevel.Info)
		
	def DropDatabases(self):
		"""Drops all databases! You must be logged out from the server first to do this.
		Returns:
			* True if all subsystems were dropped, False otherwise.
		Raises:
			* WrongModeError if we're logged into the server, or if we are in batch mode and require a password.
			* PasswordMissingError if we couldn't get credentials to drop the database with.
		"""
		#Abort if we're logged in.
		if self.LoggedIn:
			raise exceptions.WrongModeError(constants.kErrLoggedIn)
		
		#Get our password.
		if not self.promptCredentials():
			raise exceptions.PasswordMissingError(self.UserName)
		password = self.getPassword()
		
		#Drop all subsystems.
		for subsystem in self.subsystems:
			if not subsystem.Drop(self.UserName, password):
				return False
		return True