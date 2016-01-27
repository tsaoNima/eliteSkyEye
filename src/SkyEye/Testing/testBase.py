'''
Created on Jan 20, 2016

@author: Me
'''
import constants
import traceback
import time
from SkyEye.Logging import log
from SkyEye.Logging.consoleListener import ConsoleListener
from SkyEye.Logging.structs import LogLevel
from SkyEye.Exceptions.exceptions import TestFailedError

class TestResult:
	"""All functions called by DoTest must return one of the following:
	"""
	Pass = 0
	Fail = 1
	Skip = 2

class TestBase(object):
	def reset(self):
		self.numTestsAttempted = 0
		self.numTestsPassed = 0
		self.numTestsFailed = 0
		self.numTestsSkipped = 0
		#If true, test should reject any standard input.
		self.batchMode = True
	
	def onTestAllInit(self):
		"""Called before TestAll(), regardless of test success or failure.
		Standard implementation does nothing.
		"""
		
		return
	
	def onTestAllCleanup(self):
		"""Called after TestAll(), regardless of test success or failure.
		Standard implementation does nothing.
		"""
		
		return
	
	def onTestAll(self):
		"""Called when TestAll() is called. Must be implemented.
		"""
		
		raise NotImplementedError("Must implement TestAll()!")
	
	def summarizeResults(self):
		self.logSystem.LogInfo(constants.kFmtResultSummary.format(self.__class__.__name__, self.numTestsAttempted),
						constants.kTagTesting,
						constants.kMethodSummarizeResults)
		
		self.logSystem.LogInfo(constants.kFmtPassSummary.format(self.numTestsPassed),
						constants.kTagTesting,
						constants.kMethodSummarizeResults)
		if self.numTestsSkipped > 0:
			self.logSystem.LogWarning(constants.kFmtSkipSummary.format(self.numTestsSkipped),
						constants.kTagTesting,
						constants.kMethodSummarizeResults)
		if self.numTestsFailed > 0:
			self.logSystem.LogError(constants.kFmtFailSummary.format(self.numTestsFailed),
						constants.kTagTesting,
						constants.kMethodSummarizeResults)
			
		if self.numTestsPassed == self.numTestsAttempted:
			self.logSystem.LogInfo(constants.kAllPassed, constants.kTagTesting, constants.kMethodSummarizeResults)
	
	def __init__(self):
		"""Class initializer.
		"""
		
		self.logSystem = log.GetLogInstance()
		self.reset()
	
	def TestAll(self, pBatchMode=True):
		"""Runs all tests in this test module.
		"""
		#Do pre-test preparation.
		self.reset()
		self.batchMode = pBatchMode
		self.logSystem.LogDebug(constants.kFmtInitStarted.format(self.__class__.__name__),
							constants.kTagTesting,
							constants.kMethodTestAll)
		self.logSystem.LogDebug(constants.kLineSeparator, constants.kTagTesting, constants.kMethodTestAll)
		self.onTestAllInit()
		
		#Perform the test itself.
		self.logSystem.LogInfo(constants.kFmtAllTestsStarted.format(self.__class__.__name__),
							constants.kTagTesting,
							constants.kMethodTestAll)
		try:
			self.onTestAll()
		except TestFailedError:
			self.logSystem.LogError(constants.kFatalTestFailure,
								constants.kTagTesting,
								constants.kMethodTestAll)
		self.logSystem.LogInfo(constants.kLineSeparator, constants.kTagTesting, constants.kMethodTestAll)
		self.summarizeResults()
		
		#Do post-test cleanup.
		self.logSystem.LogDebug(constants.kLineSeparator, constants.kTagTesting, constants.kMethodTestAll)
		self.logSystem.LogDebug(constants.kFmtCleanupStarted.format(self.__class__.__name__),
							constants.kTagTesting,
							constants.kMethodTestAll)
		self.onTestAllCleanup()
	
	def RunStandalone(self, logPath=constants.kDefaultLogPath, logLevel=LogLevel.Verbose, pBatchMode=True):
		"""Call to run test in batch mode; this is usually the equivalent of main().
		"""
		#Prep the log system.
		self.logSystem.SetLogFile(logPath)
		listener = ConsoleListener()
		listener.SetLogLevel(logLevel)
		self.logSystem.Attach(listener)
		
		#Run all tests.
		self.TestAll(pBatchMode)
		
		#Shut the log system down now.
		self.logSystem.Shutdown()
		
	def DoTest(self, testMethod, testParams=(), where=constants.kMethodTestAll, raiseIfFailed=False):
		"""Runs the requested test, which should return a boolean.
		If the test fails, prints a failure message and optionally throws a TestFailed exception.
		"""
		methodName = testMethod.__name__
		#Mark that we're running a test.
		self.logSystem.LogInfo(constants.kFmtTestStarted.format(methodName),
							constants.kTagTesting,
							where)
		self.logSystem.LogInfo(constants.kLineSeparator,
							constants.kTagTesting,
							where)
		self.numTestsAttempted += 1
		
		testResult = None
		resultText = ""
		resultLevel = LogLevel.Info
		resultException = None
		
		#Get our test result.
		try:
			#Also see how long it takes, assuming the test passes.
			startTimeSecs = time.clock()
			testResult = testMethod(*testParams)
			endTimeSecs = time.clock()
			elapsedTimeMs = (endTimeSecs - startTimeSecs) * 1000.0
			
			#Did we pass?
			if testResult == TestResult.Pass:
				resultText = constants.kFmtTestPassed.format(methodName, elapsedTimeMs)
			#Did we fail?
			elif testResult == TestResult.Fail:
				#Note the failure.
				resultText = constants.kFmtTestFailed.format(methodName)
				#Raise any exception if we did fail.
				if raiseIfFailed:
					resultException = TestFailedError(methodName)
			#Did we skip it?
			elif testResult == TestResult.Skip:
				resultText = constants.kFmtTestSkipped.format(methodName)
		
		#Did a sub-test critically fail?
		except TestFailedError as e:
			testResult = TestResult.Fail
			resultText = constants.kFmtTestSubTestCriticalFailure.format(methodName)
		#Did an *unexpected* error occur?
		except Exception as e:
			#If any unhandled exception occurs, mark this as a failed test.
			testResult = TestResult.Fail
			resultText = constants.kFmtTestUnhandledFailure.format(methodName,
																e,
																traceback.format_exc())
			#Definitely raise an exception now, since this would ordinarily be fatal to the app.
			resultException = TestFailedError(methodName)
			
		#Now spit this info out to the logs.
		#Do level-specific actions.
		if testResult == TestResult.Pass:
			resultLevel = LogLevel.Info
			self.numTestsPassed += 1
		elif testResult == TestResult.Fail:
			resultLevel = LogLevel.Error
			self.numTestsFailed += 1
		elif testResult == TestResult.Skip:
			resultLevel = LogLevel.Warning
			self.numTestsSkipped += 1
		
		self.logSystem.Log(constants.kLineSeparator,
							resultLevel,
							constants.kTagTesting,
							where)
		self.logSystem.Log(resultText,
							resultLevel,
							constants.kTagTesting,
							where)
		#If any exception exists, raise it.
		if resultException is not None:
			raise resultException
			