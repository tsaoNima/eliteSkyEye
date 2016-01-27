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
kFmtPassSummary = "Passed: {0}"
kFmtSkipSummary = "Skipped: {0}"
kFmtFailSummary = "Failed: {0}"
kFmtResultSummary = "{0}: Total tests run: {1}"

kFmtTestStarted = "Testing {0}..."
kFmtInitStarted = "Initializing test module {0}..."
kFmtErrInitFailed = "Failed to initialize module {0}! Aborting tests!"
kFmtCleanupStarted = "Performing post-test cleanup for module {0}..."
kFmtWarnCleanupFailed = "Failed to cleanup module {0}!"
kLineSeparator = "======="
kFmtTestPassed = "{0} passed ({1} ms elapsed)."
kFmtTestFailed = "{0} failed!"
kFmtTestSkipped = "{0} skipped."
kFmtTestSubTestCriticalFailure = "A sub-test in {0} had a fatal failure, aborting {0}."
kFmtTestUnhandledFailure = "{0} failed due to unhandled exception!\nException: {1}\nDetails: {2}"