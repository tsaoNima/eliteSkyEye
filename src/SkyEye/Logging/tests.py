'''
Created on Jan 17, 2016

@author: Me
'''
import log
import consoleListener
import constants
from structs import LogLevel
from SkyEye.Testing.testBase import TestBase
from SkyEye.Testing.testBase import TestResult

class LogTests(TestBase):
	def testLogging(self):
		kMethodTestAll = "tests.TestAll()"
	
		#Get a connection to the log system.
		self.logSystem.SetLogFile("./testLogging.log")
		print "Got log instance."
		
		#Attach stdout listener.
		stdOut = consoleListener.ConsoleListener()
		stdOut.SetLogLevel(LogLevel.Verbose)
		self.logSystem.Attach(stdOut)
		print "Attached console listener."
		print "Testing log output..."
		
		#Test all levels.
		self.logSystem.LogVerbose("Verbose message.", where=kMethodTestAll)
		self.logSystem.LogDebug("Debug message.", where=kMethodTestAll)
		self.logSystem.LogInfo("Info message.", where=kMethodTestAll)
		self.logSystem.LogWarning("Warning message.", where=kMethodTestAll)
		self.logSystem.LogError("Error message.", where=kMethodTestAll)
		
		#Test tags.
		testTag = "testTag"
		stdOut.AddTag(testTag)
		self.logSystem.LogInfo("This message should be visible to stdout...", constants.kTagAll, where=kMethodTestAll)
		self.logSystem.LogInfo("But this one shouldn't!", where=kMethodTestAll)
		self.logSystem.LogInfo("This message is tagged for stdout specifically.", testTag, where=kMethodTestAll)
		
		print "Disconnecting from logger."
		self.logSystem.DetachAll()
		
		return TestResult.Pass
	
	def onTestAll(self):
		kMethod = "tests.onTestAll()"
		self.DoTest(self.testLogging, (), kMethod, True)

if __name__ == "__main__":
	LogTests().RunStandalone()