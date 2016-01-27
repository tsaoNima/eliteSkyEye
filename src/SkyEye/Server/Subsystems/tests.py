'''
Created on Jan 18, 2016

@author: Me
'''
from subsystemBase import SubsystemBase
import SkyEye.Database.schemaBase as schemaBase
from SkyEye.Testing.testBase import TestBase
from SkyEye.Testing.testBase import TestResult
from SkyEye.Logging.structs import LogLevel

class TestSchema(schemaBase.DatabaseDefinition):
	"""Describes all RDA tables.
	"""
	def __init__(self):
		self.Name = "test_db_1"
		self.AllSchemas = [
						schemaBase.TableDefinition("test_table_1",
											(schemaBase.Column("id", schemaBase.Types.Int, (schemaBase.Modifiers.PrimaryKey,)),
											schemaBase.Column("name", schemaBase.Types.VarChar, (schemaBase.Modifiers.NotNull,), schemaBase.kSchemaNameLenMax))
											),
						schemaBase.TableDefinition("test_table_2",
											(schemaBase.Column("id", schemaBase.Types.Int, (schemaBase.Modifiers.PrimaryKey,)),
											schemaBase.Column("user_id", schemaBase.Types.Int, ()),
											schemaBase.Column("elite_name", schemaBase.Types.VarChar, (), schemaBase.kSchemaNameLenMax))
											),
						schemaBase.TableDefinition("events",
										(schemaBase.Column("id", schemaBase.Types.Int, (schemaBase.Modifiers.PrimaryKey,)),
										schemaBase.Column("event_date", schemaBase.Types.Timestamp, (schemaBase.Modifiers.NotNull,)))
										)
						]

class TestSubsystem(SubsystemBase):
	def __init__(self):
		schema = TestSchema()
		super(TestSubsystem, self).__init__(schema.Name, schema)

class SubsystemTests(TestBase):	
	def testCreateAndSetup(self):
		if not self.subsystem.CreateAndSetup():
			return TestResult.Fail
		return TestResult.Pass
	
	def testStart(self):
		if not self.subsystem.Start():
			return TestResult.Fail
		return TestResult.Pass
	
	def testVerify(self):
		results = self.subsystem.Verify()
		#Verify should pass with no errors.
		if results:
			return TestResult.Fail
		return TestResult.Pass
	
	def testShutdown(self):
		self.subsystem.Shutdown()
		return TestResult.Pass
	
	def onTestAll(self):
		kMethod = "tests.TestAll()"
		self.logSystem.LogDebug("Please make sure that the server has the following database and SUPERuser:\n"
					"\tDatabase: testDB\n"
					"\tUsername: testUser\n"
					"\tPassword: testPassword\n",
					where=kMethod)
		
		self.subsystem = TestSubsystem()
		
		#Create the subsystem.
		self.DoTest(self.testCreateAndSetup)
		
		#Start the system...
		self.DoTest(self.testStart)
	
		#Do verification...
		self.DoTest(self.testVerify)
		
		#Now shut it down.
		self.DoTest(self.testShutdown)
	
if __name__ == "__main__":
	SubsystemTests().RunStandalone(logLevel=LogLevel.Info)