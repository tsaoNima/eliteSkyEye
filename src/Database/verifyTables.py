'''
Created on Jan 15, 2016

@author: Me
'''
import schemaTests
from Output import log
from Output.structs import LogLevel
from Database import constants
from Database.constants import kMethodVerifyGDW

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

def runTests(tests, results):
	for test in tests:
		passed = test[1]()
		results.addResult(test[0], passed)
		#Notify log that a schema didn't verify.
		if not passed:
			sLog.log(constants.kFmtWarnSchemaFailed % (kMethodVerifyGDW, test[0]), LogLevel.Verbose)
			
def verifyGDW():
	#Try to connect to the GDW.
	#Make sure the GDW has the following tables and that their schemas match as expected.
	testList = (("Government Type (Dimension)", schemaTests.gdwVerifyGovernmentType),
				("Economy Type (Dimension)", schemaTests.gdwVerifyEconomyType),
				("Faction (Dimension)", schemaTests.gdwVerifyFaction),
				("System (Dimension)", schemaTests.gdwVerifySystem),
				("System Celestial Structure (Dimension)", schemaTests.gdwVerifySystemCelestialStructure),
				("Structure (Dimension)", schemaTests.gdwVerifyStructure),
				("CZ Intensity (Dimension)", schemaTests.gdwVerifyCZIntensity),
				("War (Fact)", schemaTests.gdwVerifyWar),
				("Conflict Zone (Fact)", schemaTests.gdwVerifyConflictZone),
				("Faction in System (Fact)", schemaTests.gdwVerifyFactionInSystem))
	resultList = VerifyResults()
	
	#Run tests and build the result list.
	runTests(testList, resultList)
	
	return resultList
	
def verifyRDA():
	#Try to connect to the RDA.
	#Make sure the RDA has the following tables and that their schemas match as expected.
	#TODO: Following tables are optional:
	# * Player Alias Types (low priority)
	# * Player Aliases (low priority)
	testList = (("Events", schemaTests.rdaVerifyEvents),
				("Player Info", schemaTests.rdaVerifyPlayerInfo))
	resultList = VerifyResults()
	
	#Run tests and build the result list.
	runTests(testList, resultList)
	
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
			sLog.log(constants.kFmtWarnVerificationFailed % verifyTest[0], LogLevel.Warning)
			failCount += 1
			
	#Also note if everything passed!
	if failCount == 0:
		sLog.log(constants.kVerificationAllPassed, LogLevel.Info)
	
	#Now push test results into the result object.
	verifyResults = []
	for verifyTest in verifyList:
		verifyResults.append((verifyList[0], verifyList[2][0]))
	
	return (failCount, verifyResults)