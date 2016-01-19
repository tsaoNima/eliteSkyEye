'''
Created on Jan 15, 2016

@author: Me
'''
import sys
from Logging import log
from Logging import consoleListener
from Database import verifyTables
from Database import schemas
from Database import constants
from Constants import stringConstants

'''
Used to test/setup all tables in 
'''

def doSetupTables():
	mLog = log.getLogInstance()
	#Check - do we have credentials?
	#If not, ask for login.
	
	#Check each subsystem.
	subSystems = ((constants.kGDWDatabaseName, schemas.GDWSchemas()),
				(constants.kRDADatabaseName, schemas.RDASchemas()))
	#For each subsystem:
	for s in subSystems:
		#Iterate through the schemas.
		for schema in vars(s):
			#Does this schema already exist?
			#	If so, drop it.
			#Create the table.
			
	#verifyResults = verifyTables.verifyAll()
	#Did any modules fail?
	#if verifyResults[0] > 0:
	#	#If so, ask the user if they want to init failed modules to defaults.
	#	#(default to yes in batch mode)
	#	#TODO
	#	shouldReset = False
	#	#If they do want a reset...
	#	if shouldReset:
	#		#For each module:
	#		for module in verifyResults[1]:
	#		#Is this module invalid?
	#			if not module[1]:
	#				#Backup current module DB.
	#				pass
	#				#Reset the DB's schema.
	#				pass
			
class SetupTables(object):
	mLog = log.getLogInstance()
	stdOut = None
	
	def __init__(self, outPath=stringConstants.kSetupTablesDefaultOutPath):
		self.mLog.setLogFile(outPath)
		#Attach a default stdout listener.
		self.stdOut = consoleListener.ConsoleListener()
		self.mLog.attach(self.stdOut)
		
	def run(self):
		doSetupTables()
		
	def shutdown(self):
		self.mLog.shutdown()
	
#Ideally we'd have a batch mode, but we don't live in an ideal world, we live in a dangerous one. 
def main():
	mSetupTables = None
	try:
		mSetupTables = SetupTables()
	except:
		print stringConstants.kErrSetupTablesLogInitFailed
		print stringConstants.kFmtReason.format(sys.exc_info()[0])
		return
	
	mSetupTables.run()
	mSetupTables.shutdown()
	
if __name__ == '__main__':
	main()