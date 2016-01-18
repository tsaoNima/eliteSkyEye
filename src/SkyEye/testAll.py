'''
Created on Jan 17, 2016

@author: Me
'''
from Logging import log
from Logging.consoleListener import ConsoleListener
from SkyEye import Logging
from SkyEye import Database

def main():
	mLog = log.getLogInstance()
	print "Testing logger..."
	Logging.tests.testAll(mLog)
	
	#Attach our actual console listener.
	stdOut = ConsoleListener()
	mLog.attach(stdOut)
	
	mLog.logDebug("Testing database...")
	mLog.logDebug("Please make sure that the server has the following:\n"
				"\tDatabase: testDB\n"
				"\tUsername: testUser\n"
				"\tPassword: testPassword\n")
	Database.tests.testAll(mLog)
	
	#Shutdown the logger.
	mLog.shutdown()
	
if __name__ == '__main__':
	main()