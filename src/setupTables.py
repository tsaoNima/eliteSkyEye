'''
Created on Jan 15, 2016

@author: Me
'''
from Output import log
from Database import verifyTables

'''
Used to test/setup all tables in SkyEye.
'''

sLog = log.getLogInstance()

#Ideally we'd have a batch mode, but we don't live in an ideal world, we live in a dangerous one. 
def main():
	sLog.setLogFile("./setupTables.log")
	#Check each subsystem.
	#Does it have its tables?
	if not verifyTables.verifyGDW():
		#If not, init the tables now.
		#Warn the user that any data will be lost.
		pass
	
	if not verifyTables.verifyRDA():
		pass
	
if __name__ == '__main__':
	main()