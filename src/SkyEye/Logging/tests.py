'''
Created on Jan 17, 2016

@author: Me
'''
import log
import consoleListener
import constants
from structs import LogLevel

def TestAll(pLog):
	#Get a connection to the log system.
	pLog.SetLogFile("./testLogging.log")
	print "Got log instance."
	#Attach stdout listener.
	stdOut = consoleListener.ConsoleListener()
	stdOut.SetLogLevel(LogLevel.Verbose)
	pLog.Attach(stdOut)
	print "Attached console listener."
	print "Testing log output..."
	#Test all levels.
	pLog.LogVerbose("Verbose message.")
	pLog.LogDebug("Debug message.")
	pLog.LogInfo("Info message.")
	pLog.LogWarning("Warning message.")
	pLog.LogError("Error message.")
	#Test tags.
	testTag = "testTag"
	stdOut.AddTag(testTag)
	pLog.LogInfo("This message should be visible to stdout...", constants.kTagAll)
	pLog.LogInfo("But this one shouldn't!")
	pLog.LogInfo("This message is tagged for stdout specifically.", testTag)
	
	print "Disconnecting from logger."
	pLog.DetachAll()
	
if __name__ == "__main__":
	mLog = log.GetLogInstance()
	TestAll(mLog)
	mLog.Shutdown()