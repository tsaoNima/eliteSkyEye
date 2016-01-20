'''
Created on Jan 17, 2016

@author: Me
'''
import log
import consoleListener
import constants
from structs import LogLevel

def TestAll(pLog):
	kMethodTestAll = "tests.TestAll()"
	
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
	pLog.LogVerbose("Verbose message.", where=kMethodTestAll)
	pLog.LogDebug("Debug message.", where=kMethodTestAll)
	pLog.LogInfo("Info message.", where=kMethodTestAll)
	pLog.LogWarning("Warning message.", where=kMethodTestAll)
	pLog.LogError("Error message.", where=kMethodTestAll)
	#Test tags.
	testTag = "testTag"
	stdOut.AddTag(testTag)
	pLog.LogInfo("This message should be visible to stdout...", constants.kTagAll, where=kMethodTestAll)
	pLog.LogInfo("But this one shouldn't!", where=kMethodTestAll)
	pLog.LogInfo("This message is tagged for stdout specifically.", testTag, where=kMethodTestAll)
	
	print "Disconnecting from logger."
	pLog.DetachAll()
	
if __name__ == "__main__":
	mLog = log.GetLogInstance()
	TestAll(mLog)
	mLog.Shutdown()