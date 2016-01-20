'''
Created on Jan 20, 2016

@author: Me
'''
import setupTables
from SkyEye.Testing.testBase import TestBase

class ServerTests(TestBase):
	"""This test will drop any server data! Watch out!
	"""
	
	def testSetupTables(self):
		kMethodTestSetupTables = "tests.testSetupTables()"
		user = "testUser"
		password = "testPassword"
		self.logSystem.LogDebug(("Please make sure that the server has the following SUPERuser created:\n"
					"\tUsername: {0}\n"
					"\tPassword: {1}\n").format(user, password),
					where=kMethodTestSetupTables)
		
		#Run SetupDatabases first,
		#otherwise VerifyTables won't do jack.
		self.logSystem.LogDebug("Running SetupDatabases()...", where=kMethodTestSetupTables)
		setupTables.SetupDatabases(user, password)
		
		#Run VerifyTables.
		self.logSystem.LogDebug("Running VerifyTables()...", where=kMethodTestSetupTables)
		self.logSystem.LogWarning("TODO: testSetupTables() not implemented!", where=kMethodTestSetupTables)
		return False
	
		#Drop all the tables we made.
		setupTables.DropDatabases(user, password)
		
		return True

	def testServer(self):
		self.logSystem.LogWarning("TODO: testServer() not implemented!", where="tests.testServer()")
		return False
	
	def onTestAll(self):
		self.DoTest(self.testSetupTables)
		self.DoTest(self.testServer)
	
if __name__ == "__main__":
	ServerTests().BatchRun()