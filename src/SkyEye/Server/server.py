'''
Created on Jan 18, 2016

@author: Me
'''
import constants
import psycopg2
import setupTables
from .. import genericStrings
from ..Keychain import constants as KeychainConstants
from ..Database.database import Database
from ..Logging import log
from ..Keychain import keychainOps
from ..Logging.structs import LogLevel
from ..Exceptions import exceptions

sLog = log.GetLogInstance()

'''
Represents the server connection.
'''
class Server(object):
	#Database connections for subsystems.
	gdwDatabase = None
	rdaDatabase = None
	batchMode = True
	loggedIn = False
	
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
		if self.batchMode:
			#Throw an exception!
			raise exceptions.WrongModeError(genericStrings.kErrCannotPerformInBatchMode)
			return False	
		#Otherwise, ask for new login info.
		try:
			newPass = keychainOps.PromptPassword(constants.kPromptNewDBPassword)
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
			tempConnect = psycopg2.connect(database=constants.kRDADatabaseName,
										user=constants.kServerDBAdminName,
										password=pPassword)
			tempConnect.close()
			return True
		except psycopg2.Error as e:
			#If this was a password failure, we're fine.
			if e.pgcode != psycopg2.errorcodes.INVALID_PASSWORD:
				return False
			#Otherwise we need to abort.
			else:
				raise e
				return False
	
	def getCredentials(self):
		"""Returns True if we have or were able to get valid credentials,
		returns False otherwise.
		"""
		
		#First, see if we have valid credentials.
		credentialsValid = False
		#Do we have any credentials?
		if self.haveCredentials():
			#If so, try logging in.
			password = self.getPassword()
			try:
				credentialsValid = self.canLogin(password)
			except psycopg2.Error as e:
				#If a connection error occured, abort now.
				sLog.LogError(genericStrings.kFmtUnhandledError.format(e),
							constants.kTagServer,
							constants.kMethodGetCredentials)
				return False
	
		#If we don't have credentials or the credentials don't work,
		#enter new credentials loop (max 3 tries):
		if not credentialsValid:
			#Abort at this step if we're in batch mode.
			if self.batchMode:
				sLog.LogError(genericStrings.kErrCannotPerformInBatchMode,
							constants.kTagServer,
							constants.kMethodGetCredentials)
				return False
			else:
				credentialsValid = False
				for i in xrange(constants.kMaxNumPrompts):
					#Request new credentials.
					if not self.requestNewCredentials():
						sLog.LogError(constants.kErrCredentialRequestFailed,
									constants.kTagServer,
									constants.kMethodGetCredentials)
						return False
					#If the credentials work, exit loop.
					if self.canLogin(self.getPassword()):
						credentialsValid = True
						break
	
		#Do we still not have a valid login?
		if not credentialsValid:
			#Report that login attempts have been exceeded.
			sLog.LogError(constants.kErrTooManyPromptsFailed, constants.kTagServer, constants.kMethodGetCredentials)
			return False
	
	def setupLog(self, message, logLevel):
		sLog.Log(message, logLevel, constants.kTagServer, constants.kMethodFirstTimeSetup)
		print message
	
	def dropEverything(self, sysAdminDB):
		"""
		Raises:
			* InternalServiceError if any data was not successfully dropped.
		"""
		#Drop all databases.
		for subsystem in constants.kSubsystemNames:
			if not sysAdminDB.DropDatabase(subsystem):
				raise exceptions.InternalServiceError("Failed to drop database {0}!".format(subsystem))
		#Drop all users now.
		if not sysAdminDB.DropUser(constants.kServerDBAdminName):
			raise exceptions.InternalServiceError("Failed to drop user {0}!".format(constants.kServerDBAdminName))
	
	def createDBAdmin(self, sysAdminDB):
		"""
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
		if not sysAdminDB.CreateUser(constants.kServerDBAdminName,
									self.getPassword(),
									isSuperUser=True,
									canCreateDB=True):
			raise exceptions.InternalServiceError("Failed to create user {0}!".format(constants.kServerDBAdminName))
		self.setupLog(constants.kFirstTimeSetupDBAdminCreated, LogLevel.Debug)
	
	def __init__(self, pBatchMode = True):
		self.gdwDatabase = Database()
		self.rdaDatabase = Database()
		self.batchMode = True
		self.loggedIn = False
	
	def Login(self):
		"""Returns True if we successfully logged in, False otherwise.
		"""
		#If we absolutely couldn't get credentials, abort.
		if not self.getCredentials():
			sLog.LogError(constants.kErrLoginFailed, constants.kTagServer, constants.kMethodLogin)
			return False
		
		#Otherwise, connect to the databases with the credentials we got.
		gdwConnected = self.gdwDatabase.Connect(constants.kGDWDatabaseName,
								constants.kServerDBAdminName,
								self.getPassword())
		rdaConnected = self.rdaDatabase.Connect(constants.kRDADatabaseName,
								constants.kServerDBAdminName,
								self.getPassword())
		self.loggedIn = gdwConnected and rdaConnected
		#Report if all subsystems could be connected.
		if self.loggedIn:
			sLog.LogInfo(constants.kLoginComplete, constants.kTagServer, constants.kMethodLogin)
		else:
			sLog.LogError(constants.kErrLoginFailed, constants.kTagServer, constants.kMethodLogin)
		return self.loggedIn
	
	def Logout(self):
		"""Disconnects from the server.
		"""
		
		#Disconnect from subsystems.
		self.gdwDatabase.Disconnect()
		self.rdaDatabase.Disconnect()
		self.loggedIn = False
		#Report that we're logged out.
		sLog.LogInfo(constants.kLogoutComplete, constants.kTagServer, constants.kMethodLogout)
	
	def VerifyDatabases(self):
		"""Checks that all tables in the server match expected schema.
		Returns: True if all tables match expected schema, False otherwise.
		Raises:
			* WrongModeError if we're not actually logged into the server.
			* PasswordMissingError if we couldn't get the database administrator's password. 
		"""
		#Abort if we're not logged in.
		if not self.loggedIn:
			raise exceptions.WrongModeError(constants.kErrNotLoggedIn)
			return False
		
		#Get the admin login, pass that to the verify function.
		if not self.haveCredentials():
			raise exceptions.PasswordMissingError(constants.kErrNoAdminPassword)
			return False
		
		#Perform verification.
		return setupTables.VerifyDatabases(constants.kServerDBAdminName, self.getPassword())
	
	def FirstTimeSetup(self):
		"""Creates database admin account and subsystem databases for the first run.
		This can drop all existing data; back up any existing data before running this.
		Raises:
			* WrongModeError if server is in batch mode.
			* InternalServiceError if the server databases couldn't be connected to.
		"""
		
		#If we're in batch mode, quit now.
		if self.batchMode:
			raise exceptions.WrongModeError(genericStrings.kErrCannotPerformInBatchMode)
			return
		
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
				return
				
		#Clear all existing data.
		self.dropEverything(sysAdminDB)
		self.createDBAdmin(sysAdminDB)
		
		#Logout from server admin!
		sysAdminDB.Disconnect()
		
		#Login as DB admin to the system admin table.
		sysAdminDB.Connect(constants.kSysAdminDatabaseName,
						constants.kServerDBAdminName,
						self.getPassword())
		#Create subsystem databases.
		for subsystem in constants.kSubsystemNames:
			sysAdminDB.CreateDatabase(subsystem)
		
		#Logout from the system admin table!
		sysAdminDB.Disconnect()
		
		#Create all default tables.
		setupTables.SetupDatabases(constants.kServerDBAdminName, self.getPassword())
	
		#We're done!
		self.setupLog(constants.kFirstTimeSetupComplete, LogLevel.Info)