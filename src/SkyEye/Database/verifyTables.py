'''
Created on Jan 15, 2016

@author: Me
'''
import schemas
import schemaTests
from ..Logging import log
from ..Logging.structs import LogLevel
from ..Database import constants

sLog = log.getLogInstance()

class VerifyResults(object):
	mNumFailed = 0
	mTestResults = []
	
	def __init__(self):
		self.mNumFailed = 0
		self.mTestResults = []
		
	def addResult(self, testName, testResult):
		#Make sure this schema hasn't already been tested.
		for result in self.mTestResults:
			if result[0] == testName:
				return False
		self.mTestResults.append([testName, testResult])
		#Note any failed tests.
		if not testResult:
			self.mNumFailed += 1
		return True
	
	def testResults(self):
		return self.mTestResults

def runTests(database, module, results):
	for schema in vars(module):
		passed = schemaTests.verifySchema(database, schema)
		results.addResult(schema.name, passed)
		#Notify log that a schema didn't verify.
		if not passed:
			sLog.log(constants.kFmtWarnSchemaFailed.format(constants.kMethodVerifyGDW, schema.name), LogLevel.Verbose)
			
def verifyGDW():
	#Try to connect to the GDW.
	database = None
	#Make sure the GDW has the following tables and that their schemas match as expected.
	resultList = VerifyResults()
	
	#Run tests and build the result list.
	runTests(database, schemas.GDWSchemas(), resultList)
	
	return resultList
	
def verifyRDA():
	#Try to connect to the RDA.
	database = None
	#Make sure the RDA has the following tables and that their schemas match as expected.
	#TODO: Following tables are optional:
	# * Player Alias Types (low priority)
	# * Player Aliases (low priority)
	resultList = VerifyResults()
	
	#Run tests and build the result list.
	runTests(database, schemas.RDASchemas(), resultList)
	
	return resultList

'''
Verifies all data modules.
Returns:
	* A tuple:
		* First element is the number of modules that failed.
		* Second element is a list of pairs, containing the following:
			* The name of the module.
			* Another list. True if the module schema passed verification, False otherwise.
'''
def verifyAll():
	verifyList = (["GDW", verifyGDW, []], ["RDA", verifyRDA, []])
	failCount = 0
	#Run each test.
	for verifyTest in verifyList:
		verifyTest[2] = verifyTest[1]()
		#Note if this module failed verification.
		if not verifyTest[2]:
			sLog.log(constants.kFmtWarnVerificationFailed.format(verifyTest[0]), LogLevel.Warning)
			failCount += 1
			
	#Also note if everything passed!
	if failCount == 0:
		sLog.log(constants.kVerificationAllPassed, LogLevel.Info)
	
	#Now push test results into the result object.
	verifyResults = []
	for verifyTest in verifyList:
		verifyResults.append((verifyList[0], verifyList[2][0]))
	
	return (failCount, verifyResults)