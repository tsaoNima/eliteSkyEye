'''
Created on Jan 20, 2016

@author: Me
'''
from SkyEye.Testing.testBase import TestBase
from SkyEye.Testing.testBase import TestResult
from server import Server

class ServerTests(TestBase):
	"""This test will drop any server data! Watch out!
	"""
	
	def __init__(self):
		super(ServerTests, self).__init__()
		self.user = "dear_richard"
		self.server = Server()
		self.ranSetup = False
	
	def testServerLogin(self):
		#We're testing the server login process; that means we may need to ask for a password.
		#Fail if we're in batch mode, since we can't ask for a password in that mode.
		if self.batchMode:
			self.logSystem.LogError(("testServerLogin() requires interactive prompt,"
									" but test is in batch mode. Aborting test!"))
			return TestResult.Fail
		
		#Now try logging in...
		self.server.Login()
		
		return TestResult.Pass
	
	def testServerFirstTimeSetup(self):
		#This requires interactive mode; skip if in batch mode.
		if self.batchMode:
			self.logSystem.LogWarning(("testServerFirstTimeSetup() requires interactive prompt,"
									" but test is in batch mode. Skipping!"))
			return TestResult.Skip
		
		self.server.FirstTimeSetup()
		return TestResult.Pass
	
	def testServerVerify(self):
		#There should be no problems, since we just built from schema.
		problems = self.server.VerifyDatabases()
		#If we somehow did find problems, list them here
		#and mark failure.
		if problems:
			self.logSystem.LogError("Server.VerifyDatabases found {0} problems: ".format(len(problems)))
			for problem in problems:
				self.logSystem.LogError("* {0}".format(str(problem)))
			return TestResult.Fail
		
		return TestResult.Pass
	
	def testServerLogout(self):
		self.server.Logout()
		return TestResult.Pass
	
	def onTestAllInit(self):
		#Set server values.
		self.server.UserName = self.user
		self.server.BatchMode = self.batchMode
		
		#Ensure the server hasn't already been set up.
		#Clear any existing credentials.
		self.logSystem.LogDebug("Clearing test server credentials...")
		self.server.ClearCredentials()
		return True
	
	def onTestAllCleanup(self):
		self.logSystem.LogDebug("Dropping test server database and credentials...")
		#Cleanup; drop the DBs we made.
		if not self.batchMode and self.ranSetup:
			self.server.DropDatabases()
			
		#Clear server credentials.
		self.server.ClearCredentials()
		return True

	def testServer(self):
		#This requires interactive mode for the login test; skip if in batch mode.
		if self.batchMode:
			self.logSystem.LogWarning(("testServer() requires interactive prompt,"
									" but test is in batch mode. Skipping!"))
			return TestResult.Skip
				
		#Subsystems don't exist yet; perform first time setup.
		self.DoTest(self.testServerFirstTimeSetup, raiseIfFailed=True)
		self.ranSetup = True
		
		#Test logging in.
		self.DoTest(self.testServerLogin, raiseIfFailed=True)
		
		#Test verifying database.
		self.DoTest(self.testServerVerify)
		
		#Test logging out.
		self.DoTest(self.testServerLogout)
		
		return TestResult.Pass
	
	def onTestAll(self):
		self.DoTest(self.testServer)
	
if __name__ == "__main__":
	ServerTests().RunStandalone()