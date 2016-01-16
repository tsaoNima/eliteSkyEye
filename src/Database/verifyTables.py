'''
Created on Jan 15, 2016

@author: Me
'''
from Output import log
from Output.structs import LogLevel
from Database import constants

sLog = log.getLogInstance()

def verifyGDW():
	#Try to connect to the GDW.
	#Make sure the GDW has the following tables:
	#	* Government Type (Dimension)
	#	* Economy Type (Dimension)
	#	* Faction (Dimension)
	#	* System (Dimension)
	#	* System Celestial Structure (Dimension)
	#	* Structure (Dimension)
	#	* CZ Intensity (Dimension)
	#	* War (Fact)
	#	* Conflict Zone (Fact)
	#	* Faction in System (Fact)
	return False
	
def verifyRDA():
	#Try to connect to the RDA.
	#Make sure the RDA has the following tables:
	# * Events
	return False

def verifyAll():
	verifyList = (["GDW", verifyGDW, False], ["RDA", verifyRDA, False])
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