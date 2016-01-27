'''
Created on Jan 17, 2016

@author: Me
'''
from Logging import log
from Logging.consoleListener import ConsoleListener
from SkyEye import Logging
from SkyEye import Database
from SkyEye import Server
from SkyEye.Server import Subsystems

def main():
	mLog = log.GetLogInstance()
	print "Testing logger..."
	Logging.tests.LogTests().TestAll()
	
	#Attach our actual console listener.
	stdOut = ConsoleListener()
	mLog.Attach(stdOut)
	
	Database.tests.DatabaseTests().TestAll()
	Subsystems.tests.SubsystemTests().TestAll()
	Server.tests.ServerTests().TestAll()
	
	#Shutdown the logger.
	mLog.Shutdown()
	
if __name__ == '__main__':
	main()