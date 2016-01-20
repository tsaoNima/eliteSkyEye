'''
Created on Jan 18, 2016

@author: Me
'''
import database
from ..Logging import log
from ..Logging.structs import LogLevel
from ..Logging import consoleListener
from SkyEye.Server.schemas import Types
from SkyEye.Server.schemas import Modifiers
from SkyEye.Server.schemas import Schema
import SkyEye.Server.constants
from SkyEye.Testing.testBase import TestBase

class DatabaseTests(TestBase):
	dbConnection = None
	
	def testConnection(self):
		kMethod = "tests.testConnection()"
		self.logSystem.LogDebug("Attempting connection to server...", where=kMethod)
		
		self.dbConnection = database.Database()
		
		if not self.dbConnection.Connect("testDB", "testUser", "testPassword"):
			self.logSystem.LogError("Connection failed! Aborting test!", where=kMethod)
			return False
		
		return True
	
	def testTableExists(self, tableName):
		kMethod = "tests.testTableExists()"
		
		#Make sure TableExists() finds existing tables.
		if not self.dbConnection.TableExists(tableName):
			self.logSystem.LogError("Couldn't find test table \"{0}\"!".format(tableName), where=kMethod)
			return False
		
		#Make sure it can't find nonexistent tables.
		nonExistentTableName = "shouldNotExist"
		if self.dbConnection.TableExists(nonExistentTableName):
			self.logSystem.LogError("Found nonexistent table \"{0}\"!".format(nonExistentTableName), where=kMethod)
			return False
		
		return True
	
	def testDescribeTable(self, tableName):
		kMethod = "tests.testDescribeTable()"
		
		tableDesc = self.dbConnection.DescribeTable(tableName)
		if not tableDesc:
			self.logSystem.LogError("Couldn't describe table \"{0}\"!".format(tableName), where=kMethod)
			return False
		else:
			self.logSystem.LogDebug("Description of table \"{0}\":\n{1}".format(tableName, tableDesc), where=kMethod)
			
		return True
			
	def testCreateTable(self, testTableName):
		testSchema = Schema(testTableName, (
						("id", Types.int, (Modifiers.primaryKey,)),
						("var_char_column", Types.varchar, (Modifiers.notNull,), SkyEye.Server.constants.kSchemaNameLenMax),
						("bool_column", Types.bool, ())
						))
		if not self.dbConnection.CreateTable(testSchema):
			return False
	
	def testCreateRelatedTable(self, testTableName, relatedTableName):
		kMethod = "tests.testCreateRelatedTable()"
		self.logSystem.LogDebug("Creating table with foreign key...", where=kMethod)
		relatedSchema = Schema(relatedTableName,
							(
							("id", Types.int, (Modifiers.primaryKey,)),
							("test_table", Types.int, (Modifiers.notNull, (Modifiers.references, testTableName))),
							("another_column", Types.float, ())
							))
		if not self.dbConnection.CreateTable(relatedSchema):
			self.logSystem.LogError("Table w/ foreign key creation failed!", where=kMethod)
			return False
		else:
			#Try to describe the table.
			tableDesc = self.dbConnection.DescribeTable(relatedTableName)
			self.logSystem.LogDebug("Description of table \"{0}\":\n{1}".format(relatedTableName, tableDesc), where=kMethod)
		return True
	
	def testDropTable(self, testTableName, relatedTableName):
		kMethod = "tests.testDropTable()"
		
		self.dbConnection.DropTable(relatedTableName)
		#Make sure the table's actually gone.
		if self.dbConnection.TableExists(relatedTableName):
			self.logSystem.LogError("Test table \"{0}\" was not successfully dropped!".format(relatedTableName),
								 where=kMethod)
			return False
			
		#Delete the other table too.
		self.dbConnection.DropTable(testTableName)
		if self.dbConnection.TableExists(testTableName):
			self.logSystem.LogError("Test table \"{0}\" was not successfully dropped!".format(testTableName),
								 where=kMethod)
			return False
		
		return True
	
	def testTableOps(self):
		kMethod = "tests.testTableOps()"
		#Test creating a table.
		testTableName = "test_table"
		
		self.DoTest(self.testTableExists, (testTableName,), kMethod)
		
		#Test describing a table.
		self.DoTest(self.testDescribeTable, (testTableName,), kMethod)
		
		#Test creating a related table.
		relatedTableName = "related_table"
		self.DoTest(self.testCreateRelatedTable, (testTableName, relatedTableName), kMethod)
		
		#Test dropping a table.
		self.DoTest(self.testDropTable, (testTableName, relatedTableName), kMethod)
		
		return True
	
	def testCreateUser(self, newUser, newPassword):
		kMethod = "tests.testCreateUser()"
		if not self.dbConnection.CreateUser(newUser, newPassword, True, True, 7):
			self.logSystem.LogError("Could not create user {0}!".format(newUser), where=kMethod)
			return False
		
		return True
	
	def testDropUser(self, newUser):
		kMethod = "tests.testDropUser()"
		if not self.dbConnection.DropUser(newUser):
			self.logSystem.LogError("Could not drop user {0}!".format(newUser), where=kMethod)
			return False
		
		return True
	
	def testUserOps(self):
		kMethod = "tests.testUserOps()"
		
		newUser = "newTestUser"
		newPassword = "newTestPassword"
		
		#Test creating a user.
		self.DoTest(self.testCreateUser, (newUser, newPassword), where=kMethod)
			
		#Test dropping a user.
		self.DoTest(self.testDropUser, (newUser,), where=kMethod)
			
		return True
	
	def testCreateDB(self, newDBName):
		kMethod = "tests.testCreateDB()"
		
		if not self.dbConnection.CreateDatabase(newDBName):
			self.logSystem.LogError("Could not create database {0}!".format(newDBName), where=kMethod)
			return False
		
		return True
	
	def testDropDB(self, newDBName):
		kMethod = "tests.testDropDB()"
		
		if not self.dbConnection.DropDatabase(newDBName):
			self.logSystem.LogError("Could not drop database {0}!".format(newDBName), where=kMethod)
			return False
		
		return True
	
	def testDBOps(self):
		kMethod = "tests.testDBOps()"
		newDBName = "newTestDatabase"
		
		#Test creating a database.
		self.DoTest(self.testCreateDB, (newDBName,), where=kMethod)
			
		#Test dropping a database.
		self.DoTest(self.testDropDB, (newDBName,), where=kMethod)
		
		return True
	
	def onTestAll(self):
		kMethod = "tests.TestAll()"
		self.logSystem.LogDebug("Please make sure that the server has the following database and SUPERuser:\n"
					"\tDatabase: testDB\n"
					"\tUsername: testUser\n"
					"\tPassword: testPassword\n",
					where=kMethod)
		
		#Try connecting to a database.
		self.DoTest(self.testConnection, (), kMethod, True)
		
		#Test all the table operations first.
		self.DoTest(self.testTableOps, (), kMethod)
		
		#Test user operations.
		self.DoTest(self.testUserOps, (), kMethod)
		
		#Test database ops.
		self.DoTest(self.testDBOps, (), kMethod)
		
		#Disconnect our connection.
		self.logSystem.LogDebug("Closing connection to server...", where=kMethod)
		self.dbConnection.Disconnect()
	
if __name__ == "__main__":
	DatabaseTests().BatchRun()