'''
Created on Jan 18, 2016

@author: Me
'''
from ..Logging import log
import database
from schemas import Types
from schemas import Modifiers
import constants

def testAll(pLog):
	#Try connecting to a database.
	pLog.logDebug("Attempting connection to server...")
	dbConnection = database.Database()
	if not dbConnection.connect("testDB", "testUser", "testPassword"):
		pLog.logError("Connection failed! Aborting test!")
		return
	
	#Test creating a table.
	testTableName = "testTable"
	pLog.logDebug("Testing createTable()...")
	testSchema = (
					("id", Types.int, (Modifiers.primaryKey)),
					("varCharColumn", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax),
					("boolColumn", Types.bool, ())
					)
	if not dbConnection.createTable(testTableName, testSchema):
		pLog.logError("Table creation failed, aborting!")
		return
	
	#Make sure tableExists() finds existing tables
	#and can't find nonexistent tables.
	pLog.logDebug("Testing tableExists()...")
	if not dbConnection.tableExists(testTableName):
		pLog.logError("Couldn't find test table \"{0}\"!".format(testTableName))
	nonExistentTableName = "shouldNotExist"
	if dbConnection.tableExists(nonExistentTableName):
		pLog.logError("Found nonexistent table \"{0}\"!".format(nonExistentTableName))
	
	#Test describing a table.
	pLog.logDebug("Testing describeTable()...")
	tableDesc = dbConnection.describeTable(testTableName)
	if not tableDesc:
		pLog.logError("Couldn't describe table \"{0}\"!".format(testTableName))
	else:
		pLog.logDebug("Description of table \"{0}\":\n{1}".format(testTableName, tableDesc))
	
	#Test dropping a table.
	pLog.logDebug("Testing dropTable()...")
	dbConnection.dropTable(testTableName)
	#Make sure the table's actually gone.
	if dbConnection.tableExists(testTableName):
		pLog.logError("Test table \"{0}\" was not successfully dropped!".format(testTableName))
		
	#Close our connection.
	pLog.logDebug("Closing connection to server...")
	dbConnection.close()
	
if __name__ == "__main__":
	mLog = log.getLogInstance()
	testAll(mLog)
	mLog.shutdown()