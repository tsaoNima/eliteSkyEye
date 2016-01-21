'''
Created on Jan 20, 2016

@author: Me
'''
kTagTesting = "Testing"

kMethodTestAll = "TestBase.TestAll()"
kMethodSummarizeResults = "TestBase.summarizeResults()"

kDefaultLogPath = "./testResults.log"

kFmtAllTestsStarted = "Running all tests on test module {0}"
kFatalTestFailure = "Fatal test failure occurred, aborting further tests."
kAllPassed = "All tests passed."
kFmtPassSummary = "\tPassed: {0}"
kFmtSkipSummary = "\tSkipped: {0}"
kFmtFailSummary = "\tFailed: {0}"
kFmtResultSummary = "{0}:\tTotal tests run: {1}"

kFmtTestStarted = "Testing {0}..."
kFmtTestPassed = "{0} passed."
kFmtTestFailed = "{0} failed!"
kFmtTestSkipped = "{0} skipped."
kFmtTestSubTestCriticalFailure = "A sub-test in {0} had a fatal failure, aborting {0}."
kFmtTestUnhandledFailure = "{0} failed due to unhandled exception!\nException: {1}\nDetails: {2}"