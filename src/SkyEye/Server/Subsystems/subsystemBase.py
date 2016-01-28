'''
Created on Jan 25, 2016

@author: Me
'''
import constants
from SkyEye.Server import constants as serverConstants
from SkyEye.Logging import log
from SkyEye.Database.database import Database
from SkyEye.Exceptions import exceptions
from SkyEye.Exceptions.exceptions import SkyEyeError

sLog = log.GetLogInstance()

class SubsystemBase(object):
	"""Base class for server subsystems.
	Subsystems consist of a database and its respective database definition.
	"""

	def onStart(self):
		"""Called when Start() is called.
		Subclasses can override this.
		"""
		pass
	
	def onShutdown(self):
		"""Called when Shutdown() is called
		but before the database connection is closed.
		Subclasses can override this.
		"""
		pass
	
	def onSetup(self):
		"""Called in Setup(),
		after database definition has been created.		
		Subclasses can override this.
		"""
		pass
	
	def __init__(self, pName, pDefinition):
		"""Initializer.
		"""
		
		self.Database = Database()
		self.Definition = pDefinition
		self.Name = pName
	
	def CreateAndSetup(self, userName, password):
		"""Creates the database for this subsystem.
		Returns: True if the database was created and is ready for operation,
		False otherwise.
		Raises:
			* InternalServiceError if self.Definition is not set. 
		"""
		
		#Abort if no definition is set.
		if self.Definition is None:
			raise exceptions.InternalServiceError(constants.kErrFmtCreateNeedsDBDefinition.format(self.Name))
		
		#Connect to the sysadmin database.
		adminDB = Database()
		try:
			adminDB.Connect(serverConstants.kSysAdminDatabaseName, userName, password)
			
			#Make the CREATE DATABASE call.
			if not adminDB.CreateDatabase(self.Definition.Name):
				return False
			
			#Logout.
			adminDB.Disconnect()
		#If anything bad happened, close connection and assume failure.
		except SkyEyeError as e:
			sLog.LogError("Unexpected error: {0}".format(e), constants.kTagSubsystemBase, "SubsystemBase.CreateAndSetup()")
			#Try to disconnect the DB.
			adminDB.Disconnect()
			return False
		
		try:
			#Log in to the subsystem's database.
			#Run self.Setup().
			self.Database.Connect(self.Definition.Name, userName, password)
			self.Setup()
			self.Database.Disconnect()
		#If anything bad happened, close connection and assume failure.
		except SkyEyeError as e:
			sLog.LogError("Unexpected error: {0}".format(e), constants.kTagSubsystemBase, "SubsystemBase.CreateAndSetup()")
			#Try to disconnect the DB.
			self.Database.Disconnect()
			return False
		
		#Otherwise we're done!
		return True
	
	def Drop(self, userName, password):
		"""Drops this subsystem's database!
		Returns: True if the database was dropped, False otherwise.
		Raises:
			* InternalServiceError if self.Definition is not set.
		"""
		#Abort if no definition is set.
		if self.Definition is None:
			raise exceptions.InternalServiceError(constants.kErrFmtDropNeedsDBDefinition.format(self.Name))
		
		#Connect to the sysadmin database.
		adminDB = Database()
		try:
			adminDB.Connect(serverConstants.kSysAdminDatabaseName, userName, password)
			
			#Make the CREATE DATABASE call.
			if not adminDB.DropDatabase(self.Definition.Name):
				return False
			
			#Logout.
			adminDB.Disconnect()
		#If anything bad happened, close connection and assume failure.
		except SkyEyeError as e:
			sLog.LogError("Unexpected error: {0}".format(e), constants.kTagSubsystemBase, "SubsystemBase.CreateAndSetup()")
			#Try to disconnect the DB.
			adminDB.Disconnect()
			return False
		
		return True
	
	def Setup(self):
		"""Calls SetupDatabase on the subsystem. Any existing data may be lost.
		Returns:
			* True if the database was successfully setup, False otherwise.
		Raises:
			* InternalServiceError if self.Definition is not set.
		"""
		
		if self.Definition is None:
			raise exceptions.InternalServiceError(constants.kErrFmtSetupNeedsDBDefinition.format(self.Name))
		
		if not self.Database.SetupDatabase(self.Definition):
			return False
		self.onSetup()
		
	def Verify(self):
		"""Calls VerifyDatabase on the subsystem.
		Returns:
			* A list of any verification problems with the subsystem's database.
		Raises:
			* InternalServiceError if self.Definition is not set.
		"""
		
		if self.Definition is None:
			raise exceptions.InternalServiceError(constants.kErrFmtVerifyNeedsDBDefinition.format(self.Name))
		
		return self.Database.VerifyDatabase(self.Definition)
		
	def Start(self, userName, password):
		"""Called to prepare the subsystem for operation.
		Raises:
			* PaswordInvalidError if the given password was invalid.
			* InternalServiceError if any other connection error occurred.
		"""
		sLog.LogDebug(constants.kFmtStartingSubsystem.format(self.Name),
					constants.kTagSubsystemBase,
					constants.kMethodStart)
		
		if self.Definition is None:
			raise exceptions.InternalServiceError(constants.kErrFmtStartNeedsDBDefinition.format(self.Name))
		
		#Connect to the database.
		self.Database.Connect(self.Definition.Name, userName, password)
		
		#Do subclass-specific work.
		self.onStart()
		
		#We're done!
		sLog.LogDebug(constants.kFmtStartedSubsystem.format(self.Name),
					constants.kTagSubsystemBase,
					constants.kMethodStart)
	
	def Shutdown(self):
		"""Called to release active resources and halt operation.
		"""
		
		sLog.LogDebug(constants.kFmtShuttingDownSubsystem.format(self.Name),
					constants.kTagSubsystemBase,
					constants.kMethodStart)
		
		#Do subclass-specific work.
		self.onShutdown()
		
		self.Database.Disconnect()
		
		sLog.LogDebug(constants.kFmtShutDownSubsystem.format(self.Name),
					constants.kTagSubsystemBase,
					constants.kMethodStart)