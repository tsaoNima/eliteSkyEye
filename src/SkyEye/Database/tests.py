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
	testDBName = "test_db"
	createDBName = "new_db"
	verifyDBName = "new_db_2"
	
	def testConnection(self):
		kMethod = "tests.testConnection()"
		self.logSystem.LogDebug("Attempting connection to server...", where=kMethod)
		
		self.dbConnection = database.Database()
		
		if not self.dbConnection.Connect(self.testDBName, "testUser", "testPassword"):
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
						Column("id", Types.Int, (Modifiers.PrimaryKey,)),
						Column("var_char_column", Types.VarChar, (Modifiers.Unique,), 255),
						Column("bool_column", Types.Bool, ())
						))
		if not self.dbConnection.CreateTable(testSchema):
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testCreateRelatedTable(self, testTableName, relatedTableName):
		kMethod = "tests.testCreateRelatedTable()"
		self.logSystem.LogDebug("Creating table with foreign key...", where=kMethod)
		relatedSchema = TableDefinition(relatedTableName,
							(
							Column("id", Types.Int, (Modifiers.PrimaryKey,)),
							Column("test_table", Types.Int, (Modifiers.NotNull,), pForeignKey=testTableName),
							Column("another_column", Types.Float, ())
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
	
	def testCreateDB(self):
		kMethod = "tests.testCreateDB()"
		
		if not self.dbConnection.CreateDatabase(self.createDBName):
			self.logSystem.LogError("Could not create database {0}!".format(self.createDBName),
								where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testDropDB(self):
		kMethod = "tests.testDropDB()"
		
		if not self.dbConnection.DropDatabase(self.createDBName):
			self.logSystem.LogError("Could not drop database {0}!".format(self.createDBName),
								where=kMethod)
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testSetupAndVerifyDB(self):
		kMethod = "tests.testSetupAndVerifyDB()"
		kDBDefinition = schemaBase.DatabaseDefinition()
		kDBDefinition.Name = self.verifyDBName
		kDBDefinition.AllSchemas = [
								TableDefinition("table_1",
									(
									Column("id", Types.Int, (Modifiers.PrimaryKey,)),
									Column("name", Types.VarChar, (Modifiers.NotNull,), pPrecision = 32),
									Column("date", Types.Timestamp, ())
									)),
								TableDefinition("table_2",
									(
									Column("id", Types.Int, (Modifiers.PrimaryKey,)),
									Column("table_1_foreign_a", Types.Int, (Modifiers.NotNull,), pForeignKey="table_1"),
									Column("table_1_foreign_b", Types.Int, pForeignKey="table_1", pUpdateRule=schemaBase.DeleteUpdateModifiers.Cascade),
									)),
								TableDefinition("unrelated_table",
									(
									Column("id", Types.Int, (Modifiers.PrimaryKey,)),
									Column("bool", Types.Bool),
									Column("char", Types.Char, pPrecision = 32),
									Column("float", Types.Float, (Modifiers.Unique,)),
									Column("date", Types.Date),
									Column("real", Types.Real)
									))
								]
		
		kDBBadDefinition = schemaBase.DatabaseDefinition()
		kDBBadDefinition.Name = self.verifyDBName
		kDBBadDefinition.AllSchemas = [
								TableDefinition("table_1",
									(
									Column("id", Types.Int, (Modifiers.PrimaryKey,)),
									Column("name", Types.VarChar, (Modifiers.NotNull,), pPrecision = 32),
									Column("date", Types.Timestamp, ())
									)),
								TableDefinition("should_not_exist",
									(
									Column("id", Types.Int, (Modifiers.PrimaryKey,)),
									)),
								TableDefinition("unrelated_table",
									(
									Column("id", Types.Int, (Modifiers.PrimaryKey,)),
									Column("col_should_not_exist", Types.Int, pForeignKey="table_1"),
									Column("char", Types.Char, pPrecision = 48),
									Column("float", Types.Float, (Modifiers.Unique,)),
									Column("date", Types.Date),
									Column("real", Types.Real)
									))
								]
		
		#Create this new DB.
		self.dbConnection.CreateDatabase(kDBDefinition.Name)
		
		newDB = database.Database()
		newDB.Connect(kDBDefinition.Name, "testUser", "testPassword")
		#First, test setting up the DB.
		#The DB must exist, of course.
		if not newDB.SetupDatabase(kDBDefinition):
			self.logSystem.LogError("Could not setup database {0}!".format(kDBDefinition.Name), where=kMethod)
			return TestResult.Fail
		
		#Next, test verifying the DB.
		results = newDB.VerifyDatabase(kDBDefinition)
		if results:
			self.logSystem.LogError("Could not verify database {0}!".format(kDBDefinition.Name), where=kMethod)
			#List the errors found.
			self.logSystem.LogError("Reported errors:", where=kMethod)
			for problem in results:
				self.logSystem.LogError("* {0}".format(str(problem)), where=kMethod)
			return TestResult.Fail
		
		#Now make sure verifications can fail.
		results = newDB.VerifyDatabase(kDBBadDefinition)
		#Fail if it says there are NO errors.
		if not results:
			self.logSystem.LogError("Verification functions are not verifying properly!", where=kMethod)
			return TestResult.Fail
		
		#List the errors found.
		self.logSystem.LogVerbose("Successfully checked verification functions.", where=kMethod)
		self.logSystem.LogVerbose("Reported {0} errors:".format(len(results)), where=kMethod)
		for problem in results:
			self.logSystem.LogVerbose("* {0}".format(str(problem)), where=kMethod)
		
		newDB.Disconnect()
		
		#Drop the DB we made.
		self.dbConnection.DropDatabase(kDBDefinition.Name)
		
		return TestResult.Pass
	
	def testDBOps(self):
		kMethod = "tests.testDBOps()"
		
		#Test creating a database.
		self.DoTest(self.testCreateDB, where=kMethod)
			
		#Test dropping a database.
		self.DoTest(self.testDropDB, where=kMethod)
		
		#Test verifying a database.
		self.DoTest(self.testSetupAndVerifyDB, where=kMethod)
		
		return TestResult.Pass
	
	def onTestAllInit(self):
		#Prep the system; ensure any test databases don't already exist.
		self.logSystem.LogDebug("Resetting databases for test...")
		adminDB = database.Database()
		adminDB.Connect("postgres", "testUser", "testPassword")
		adminDB.DropDatabase(self.verifyDBName)
		adminDB.DropDatabase(self.createDBName)
		adminDB.DropDatabase(self.testDBName)
		adminDB.CreateDatabase(self.testDBName)
		adminDB.Disconnect()
		self.logSystem.LogDebug("Test Databases reset.")
	
	def onTestAllCleanup(self):
		#Cleanup; delete testDB.
		self.logSystem.LogDebug("Cleanup - dropping test databases...")
		adminDB = database.Database()
		adminDB.Connect("postgres", "testUser", "testPassword")
		adminDB.DropDatabase(self.verifyDBName)
		adminDB.DropDatabase(self.createDBName)
		adminDB.DropDatabase(self.testDBName)
		adminDB.Disconnect()
		self.logSystem.LogDebug("Test databases dropped.")
	
	def onTestAll(self):
		kMethod = "tests.TestAll()"
		self.logSystem.LogDebug("Please make sure that the server has the following SUPERuser:\n"
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
	DatabaseTests().RunStandalone(logLevel=LogLevel.Verbose)