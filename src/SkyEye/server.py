'''
Created on Jan 18, 2016

@author: Me
'''
import genericStrings
import constants
import Keychain.constants
import Database.constants
import psycopg2
from Database import setupTables
from Logging import log
from Keychain import keychainOps
from SkyEye.constants import kMaxNumPrompts

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
		return keychainOps.GetPassword(Keychain.constants.kServiceDatabase)
	
	def haveCredentials(self):
		return self.getPassword() is not None
	
	def requestNewCredentials(self):
		"""Returns True if given new credentials, returns False otherwise.
		"""
		
		#Are we in batch mode?
		if self.batchMode:
			#If true, fail.
			sLog.LogError(genericStrings.kErrCannotPerformInBatchMode,
						constants.kTagServer,
						constants.kMethodRequestNewCredentials)
			return False	
		#Otherwise, ask for new login info.
		try:
			newPass = keychainOps.RequestPassword(constants.kPromptNewDBPassword)
			keychainOps.SetPassword(Keychain.constants.kServiceDatabase, newPass)
			return True
		except Exception as e:
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
			tempConnect = psycopg2.connect(database=Database.constants.kRDADatabaseName,
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
				for i in xrange(kMaxNumPrompts):
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
		return self.loggedIn
	
	def FirstTimeSetup(self):
		#Login loop:
		#	Ask for the admin password to the DB. DO NOT STORE THIS.
		#	Logon to "postgres" as the admin "postgres".
		
		#Create our DB admin. Ask for DB admin password.
		#Perform the CREATE USER query. This is the DB admin,
		#so it should have rights to create a database.
		#Store DB admin password in keychain.
		
		#Logout from server admin!
		
		#Login as DB admin.
		#Create all default tables.
		setupTables.SetupTables(user, password)
		#Ideally, fill in the tables with default data.
		pass
	
	def VerifyTables(self):
		#Abort if we're not logged in.
		
		#Get the admin login, pass that to the verify function.
		return setupTables.VerifyTables(user, password)
	
	def Logout(self):
		#Disconnect from subsystems.
		self.loggedIn = False