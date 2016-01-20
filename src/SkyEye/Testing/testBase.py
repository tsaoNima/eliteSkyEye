'''
Created on Jan 20, 2016

@author: Me
'''
import constants

from SkyEye.Logging import log
from SkyEye.Logging.consoleListener import ConsoleListener
from SkyEye.Logging.structs import LogLevel
from SkyEye.Exceptions.exceptions import TestFailedError

class TestBase(object):
	logSystem = None
	numTestsAttempted = 0
	numTestsFailed = 0
	
	def reset(self):
		self.numTestsAttempted = 0
		self.numTestsFailed = 0
	
	def onTestAll(self):
		"""Called when TestAll() is called. Must be implemented.
		"""
		
		raise NotImplementedError("Must implement TestAll()!")
	
	def summarizeResults(self):
		resultText = constants.kAllPassedSummary
		resultLevel = LogLevel.Info
		
		if self.numTestsFailed > 0:
			resultText = constants.kFmtPassFailSummary.format(self.numTestsAttempted - self.numTestsFailed,
														self.numTestsFailed)
			resultLevel = LogLevel.Error
			
		self.logSystem.Log(constants.kFmtResultSummary.format(self.__class__.__name__, self.numTestsAttempted, resultText),
						resultLevel,
						constants.kTagTesting,
						constants.kMethodSummarizeResults)
	
	def __init__(self):
		"""Class initializer.
		"""
		
		self.logSystem = log.GetLogInstance()
		self.reset()
	
	def TestAll(self):
		"""Runs all tests in this test module.
		"""
		self.reset()
		self.logSystem.LogInfo(constants.kFmtAllTestsStarted.format(self.__class__.__name__),
							constants.kTagTesting,
							constants.kMethodTestAll)
		try:
			self.onTestAll()
		except TestFailedError:
			self.logSystem.LogError(constants.kFatalTestFailure,
								constants.kTagTesting,
								constants.kMethodTestAll)
		except Exception:
			self.logSystem.LogError(constants.kUnhandledFailure,
								constants.kTagTesting,
								constants.kMethodTestAll)
		self.summarizeResults()
	
	def BatchRun(self, logPath=constants.kDefaultLogPath, logLevel=LogLevel.Verbose):
		"""Call to run test in batch mode; this is usually the equivalent of main().
		"""
		#Prep the log system.
		self.logSystem.SetLogFile(logPath)
		listener = ConsoleListener()
		listener.SetLogLevel(LogLevel.Verbose)
		self.logSystem.Attach(listener)
		
		#Run all tests.
		self.TestAll()
		
		#Shut the log system down now.
		self.logSystem.Shutdown()
		
	def DoTest(self, testMethod, testParams=(), where=constants.kMethodTestAll, raiseIfFailed=False):
		"""Runs the requested test, which should return a boolean.
		If the test fails, prints a failure message and optionally throws a TestFailed exception.
		"""
		methodName = testMethod.__name__
		#Mark that we're running a test.
		self.logSystem.LogInfo(constants.kFmtTestStarted.format(methodName), constants.kTagTesting, where)
		self.numTestsAttempted += 1
		
		#If we failed...
		if not testMethod(*testParams):
			#Note the failure.
			self.numTestsFailed += 1
			self.logSystem.LogError(constants.kFmtTestFailed.format(methodName), constants.kTagTesting, where)
			#Raise any exception if we did fail.
			if raiseIfFailed:
				raise TestFailedError(methodName)