'''
Created on Jan 20, 2016

@author: Me
'''
from SkyEye.Logging import log
from SkyEye.Logging.consoleListener import ConsoleListener
from SkyEye.Logging.structs import LogLevel
import setupTables

sLog = log.GetLogInstance()

def testSetupTables():
	kMethodTestSetupTables = "tests.testSetupTables()"
	user = "testUser"
	password = "testPassword"
	sLog.LogDebug(("Please make sure that the server has the following SUPERuser created:\n"
				"\tUsername: {0}\n"
				"\tPassword: {1}\n").format(user, password),
				where=kMethodTestSetupTables)
	
	#Run SetupTables first,
	#otherwise VerifyTables won't do jack.
	sLog.LogDebug("Running SetupTables()...", where=kMethodTestSetupTables)
	setupTables.SetupTables(user, password)
	
	#Run VerifyTables.
	sLog.LogDebug("Running VerifyTables()...", where=kMethodTestSetupTables)
	sLog.LogWarning("TODO: testSetupTables() not implemented!", where=kMethodTestSetupTables)
	pass

def testServer():
	sLog.LogWarning("TODO: testServer() not implemented!", where="tests.testServer()")
	pass

def TestAll():
	sLog.LogVerbose("Testing setupTables.py calls...", where="tests.TestAll()")
	testSetupTables()
	sLog.LogVerbose("Testing server.py calls...", where="tests.TestAll()")
	testServer()
	
def main():
	listener = ConsoleListener()
	listener.SetLogLevel(LogLevel.Verbose)
	sLog.Attach(listener)
	
	TestAll()
	
	sLog.Shutdown()