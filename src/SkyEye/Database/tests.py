'''
Created on Jan 18, 2016

@author: Me
'''
import database
from SkyEye.Database import schemaBase
from ..Logging.structs import LogLevel
from SkyEye.Database.schemaBase import Types
from SkyEye.Database.schemaBase import Modifiers
from SkyEye.Database.schemaBase import TableDefinition
from SkyEye.Database.schemaBase import Column
from SkyEye.Testing.testBase import TestBase
from SkyEye.Testing.testBase import TestResult

class DatabaseTests(TestBase):
	dbConnection = None
	
	def testConnection(self):
		kMethod = "tests.testConnection()"
		self.logSystem.LogDebug("Attempting connection to server...", where=kMethod)
		
		self.dbConnection = database.Database()
		
		if not self.dbConnection.Connect("testDB", "testUser", "testPassword"):
			self.logSystem.LogError("Connection failed! Aborting test!", where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testTableExists(self, tableName):
		kMethod = "tests.testTableExists()"
		
		#Make sure TableExists() finds existing tables.
		if not self.dbConnection.TableExists(tableName):
			self.logSystem.LogError("Couldn't find test table \"{0}\"!".format(tableName), where=kMethod)
			return TestResult.Fail
		
		#Make sure it can't find nonexistent tables.
		nonExistentTableName = "shouldNotExist"
		if self.dbConnection.TableExists(nonExistentTableName):
			self.logSystem.LogError("Found nonexistent table \"{0}\"!".format(nonExistentTableName), where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testDescribeTable(self, tableName):
		kMethod = "tests.testDescribeTable()"
		
		tableDesc = self.dbConnection.DescribeTable(tableName)
		if not tableDesc:
			self.logSystem.LogError("Couldn't describe table \"{0}\"!".format(tableName), where=kMethod)
			return TestResult.Fail
		else:
			self.logSystem.LogDebug("Description of table \"{0}\":\n{1}".format(tableName, tableDesc), where=kMethod)
			
		return TestResult.Pass
			
	def testCreateTable(self, testTableName):
		testSchema = TableDefinition(testTableName, (
						Column("id", Types.int, (Modifiers.primaryKey,)),
						Column("var_char_column", Types.varchar, (Modifiers.unique,), 255),
						Column("bool_column", Types.bool, ())
						))
		if not self.dbConnection.CreateTable(testSchema):
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testCreateRelatedTable(self, testTableName, relatedTableName):
		kMethod = "tests.testCreateRelatedTable()"
		self.logSystem.LogDebug("Creating table with foreign key...", where=kMethod)
		relatedSchema = TableDefinition(relatedTableName,
							(
							Column("id", Types.int, (Modifiers.primaryKey,)),
							Column("test_table", Types.int, (Modifiers.notNull, (Modifiers.references, testTableName))),
							Column("another_column", Types.float, ())
							))
		if not self.dbConnection.CreateTable(relatedSchema):
			self.logSystem.LogError("Table w/ foreign key creation failed!", where=kMethod)
			return TestResult.Fail
		else:
			#Try to describe the table.
			tableDesc = self.dbConnection.DescribeTable(relatedTableName)
			self.logSystem.LogDebug("Description of table \"{0}\":\n{1}".format(relatedTableName, tableDesc), where=kMethod)
		return TestResult.Pass
	
	def testDropTable(self, testTableName, relatedTableName):
		kMethod = "tests.testDropTable()"
		
		self.dbConnection.DropTable(relatedTableName)
		#Make sure the table's actually gone.
		if self.dbConnection.TableExists(relatedTableName):
			self.logSystem.LogError("Test table \"{0}\" was not successfully dropped!".format(relatedTableName),
								 where=kMethod)
			return TestResult.Fail
			
		#Delete the other table too.
		self.dbConnection.DropTable(testTableName)
		if self.dbConnection.TableExists(testTableName):
			self.logSystem.LogError("Test table \"{0}\" was not successfully dropped!".format(testTableName),
								 where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testTableOps(self):
		kMethod = "tests.testTableOps()"
		#Test creating a table.
		testTableName = "test_table"
		self.DoTest(self.testCreateTable, (testTableName,), kMethod)
		
		#Table existence...
		self.DoTest(self.testTableExists, (testTableName,), kMethod)
		
		#Test describing a table.
		self.DoTest(self.testDescribeTable, (testTableName,), kMethod)
		
		#Test creating a related table.
		relatedTableName = "related_table"
		self.DoTest(self.testCreateRelatedTable, (testTableName, relatedTableName), kMethod)
		
		#Test dropping a table.
		self.DoTest(self.testDropTable, (testTableName, relatedTableName), kMethod)
		
		return TestResult.Pass
	
	def testCreateUser(self, newUser, newPassword):
		kMethod = "tests.testCreateUser()"
		if not self.dbConnection.CreateUser(newUser, newPassword, True, True, 7):
			self.logSystem.LogError("Could not create user {0}!".format(newUser), where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testDropUser(self, newUser):
		kMethod = "tests.testDropUser()"
		if not self.dbConnection.DropUser(newUser):
			self.logSystem.LogError("Could not drop user {0}!".format(newUser), where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testUserOps(self):
		kMethod = "tests.testUserOps()"
		
		newUser = "newTestUser"
		newPassword = "newTestPassword"
		
		#Test creating a user.
		self.DoTest(self.testCreateUser, (newUser, newPassword), where=kMethod)
			
		#Test dropping a user.
		self.DoTest(self.testDropUser, (newUser,), where=kMethod)
			
		return TestResult.Pass
	
	def testCreateDB(self, newDBName):
		kMethod = "tests.testCreateDB()"
		
		if not self.dbConnection.CreateDatabase(newDBName):
			self.logSystem.LogError("Could not create database {0}!".format(newDBName), where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testDropDB(self, newDBName):
		kMethod = "tests.testDropDB()"
		
		if not self.dbConnection.DropDatabase(newDBName):
			self.logSystem.LogError("Could not drop database {0}!".format(newDBName), where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testSetupAndVerifyDB(self, currentDBName):
		kMethod = "tests.testSetupAndVerifyDB()"
		kDBDefinition = schemaBase.DatabaseDefinition()
		kDBDefinition.Name = currentDBName
		kDBDefinition.AllSchemas = [
								TableDefinition("table_1",
									(
									Column("id", Types.int, (Modifiers.primaryKey,)),
									Column("name", Types.varchar, (Modifiers.notNull,), 32),
									Column("date", Types.timestamp, ())
									)),
								TableDefinition("table_2",
									(
									Column("id", Types.int, (Modifiers.primaryKey,)),
									Column("table_1_foreign_a", Types.int, (Modifiers.notNull,), pForeignKey="table_1"),
									Column("table_1_foreign_b", Types.int, (Modifiers.onUpdateCascade), pForeignKey="table_1"),
									)),
								TableDefinition("unrelated_table",
									(
									Column("id", Types.int, (Modifiers.primaryKey,)),
									Column("bool", Types.bool),
									Column("char", Types.char, 32),
									Column("float", Types.float, (Modifiers.unique,)),
									Column("date", Types.date),
									Column("real", Types.real)
									))
								]
		
		#First, test setting up the DB.
		#The DB must exist, of course.
		if not self.dbConnection.SetupDatabase(kDBDefinition):
			self.logSystem.LogError("Could not setup database {0}!".format(kDBDefinition.Name), where=kMethod)
			return TestResult.Fail
		
		#Next, test verifying the DB.
		pass
		if not self.dbConnection.VerifyDatabase(kDBDefinition):
			self.logSystem.LogError("Could not verify database {0}!".format(kDBDefinition.Name), where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testDBOps(self):
		kMethod = "tests.testDBOps()"
		currentDBName = "testDB"
		newDBName = "newTestDatabase"
		
		#Test creating a database.
		self.DoTest(self.testCreateDB, (newDBName,), where=kMethod)
			
		#Test dropping a database.
		self.DoTest(self.testDropDB, (newDBName,), where=kMethod)
		
		#Test verifying a database.
		self.DoTest(self.testSetupAndVerifyDB, (currentDBName,), where=kMethod)
		
		return TestResult.Pass
	
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
	DatabaseTests().RunStandalone(logLevel=LogLevel.Info)