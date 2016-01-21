'''
Created on Jan 20, 2016

@author: Me
'''
import setupTables
from SkyEye.Testing.testBase import TestBase
from SkyEye.Testing.testBase import TestResult

class ServerTests(TestBase):
	"""This test will drop any server data! Watch out!
	"""
	
	def __init__(self):
		super(ServerTests, self).__init__()
		self.user = "testUser"
		self.password = "testPassword"
	
	def testSetupDatabases(self):
		setupTables.SetupDatabases(self.user, self.password)
		return TestResult.Pass
	
	def testVerifyDatabases(self):
		problems = setupTables.VerifyDatabases(self.user, self.password)
		#This was just built from schema, so it has to fully verify.
		if problems:
			self.logSystem.LogError("VerifyDatabases() detected the following problems: ")
			for p in problems:
				self.logSystem.LogError(p)
			return TestResult.Fail
		
		return TestResult.Pass
		
	def testSetupTables(self):
		kMethodTestSetupTables = "tests.testSetupTables()"
		
		self.logSystem.LogDebug(("Please make sure that the server has the following SUPERuser created:\n"
					"\tUsername: {0}\n"
					"\tPassword: {1}\n").format(self.user, self.password),
					where=kMethodTestSetupTables)
		
		#Run SetupDatabases first,
		#otherwise VerifyTables won't do jack.
		self.DoTest(self.testSetupDatabases)
		
		#Run VerifyTables.
		self.DoTest(self.testVerifyDatabases)
	
		#Drop all the tables we made.
		#setupTables.DropDatabases(self.user, self.password)
		
		return TestResult.Pass
	
	def testServerLogin(self):
		self.logSystem.LogWarning("TODO: testServerLogin() not implemented!")
		return TestResult.Fail
	
	def testServerFirstTimeSetup(self):
		#This requires interactive mode; skip if in batch mode.
		if self.batchMode:
			self.logSystem.LogWarning(("testServerFirstTimeSetup() requires interactive prompt,"
									" but test is in batch mode. Skipping!"))
			return TestResult.Skip
		
		self.logSystem.LogWarning("TODO: testServerFirstTimeSetup() not implemented!")
		return TestResult.Fail
	
	def testServerVerify(self):
		self.logSystem.LogWarning("TODO: testServerVerify() not implemented!")
		return TestResult.Fail
	
	def testServerLogout(self):
		self.logSystem.LogWarning("TODO: testServerLogout() not implemented!")
		return TestResult.Fail

	def testServer(self):
		self.logSystem.LogWarning("TODO: testServer() not implemented!", where="tests.testServer()")
		
		#Test logging in.
		self.DoTest(self.testServerLogin, raiseIfFailed=True)
		
		#Test first time setup.
		self.DoTest(self.testServerFirstTimeSetup)
		
		#Test verifying database.
		self.DoTest(self.testServerVerify)
		
		#Test logging out.
		self.DoTest(self.testServerLogout)
		
		return TestResult.Pass
	
	def onTestAll(self):
		self.DoTest(self.testSetupTables)
		self.DoTest(self.testServer)
	
if __name__ == "__main__":
	ServerTests().RunStandalone()