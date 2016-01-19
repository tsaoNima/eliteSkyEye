'''
Created on Jan 17, 2016

@author: Me
'''
from Logging import log
from Logging.consoleListener import ConsoleListener
from SkyEye import Logging
from SkyEye import Database

def main():
	mLog = log.GetLogInstance()
	print "Testing logger..."
	Logging.tests.TestAll(mLog)
	
	#Attach our actual console listener.
	stdOut = ConsoleListener()
	mLog.Attach(stdOut)
	
	mLog.LogDebug("Testing database...")
	Database.tests.TestAll(mLog)
	
	#Shutdown the logger.
	mLog.Shutdown()
	
if __name__ == '__main__':
	main()