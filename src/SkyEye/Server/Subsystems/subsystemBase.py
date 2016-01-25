'''
Created on Jan 25, 2016

@author: Me
'''
from SkyEye.Database.database import Database
from SkyEye.Exceptions import exceptions

class SubsystemBase(object):
	"""Base class for server subsystems.
	Subsystems consist of a database and its respective database definition.
	"""

	def __init__(self, pName, pDefinition):
		"""Initializer.
		"""
		
		self.Database = Database()
		self.Definition = pDefinition
		self.Name = pName
	
	def Create(self, userName, password):
		"""Creates the database for this subsystem.
		"""
		
		#Connect to the sysadmin database.
		#Make the CREATE DATABASE call.
		#Logout.
		pass
	
	def Setup(self):
		"""Calls SetupDatabase on the subsystem. Any existing data may be lost.
		Returns:
			* True if the database was successfully setup, False otherwise.
		Raises:
			* InternalServiceError if self.Definition is not set.
		"""
		
		if self.Definition is None:
			raise exceptions.InternalServiceError("Database definition not set, can't setup subsystem {0}!".format(self.Name))
		
		return self.Database.SetupDatabase(self.Definition)
		
	def Verify(self):
		"""Calls VerifyDatabase on the subsystem.
		Returns:
			* A list of any verification problems with the subsystem's database.
		Raises:
			* InternalServiceError if self.Definition is not set.
		"""
		
		if self.Definition is None:
			raise exceptions.InternalServiceError("Database definition not set, can't verify subsystem {0}!".format(self.Name))
		
		return self.Database.VerifyDatabase(self.Definition)
		
	def Start(self, userName, password):
		"""Called to prepare the subsystem for operation.
		Raises:
			* PaswordInvalidError if the given password was invalid.
			* InternalServiceError if any other connection error occurred.
		"""
		
		if self.Definition is None:
			raise exceptions.InternalServiceError("Database definition not set, can't connect subsystem {0}!".format(self.Name))
		
		#Connect to the database.
		self.Database.Connect(self.Definition.Name, userName, password)
	
	def Shutdown(self):
		"""Called to release active resources and halt operation.
		"""
		
		self.Database.Disconnect()
		pass