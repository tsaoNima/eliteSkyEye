'''
Created on Jan 18, 2016

@author: Me
'''
import database
import constants
from ..Logging import log
from ..Logging.structs import LogLevel
from ..Logging import consoleListener
from schemas import Types
from schemas import Modifiers
from schemas import Schema

def testAll(pLog):
	pLog.logDebug("Please make sure that the server has the following:\n"
				"\tDatabase: testDB\n"
				"\tUsername: testUser\n"
				"\tPassword: testPassword\n")
	
	#Try connecting to a database.
	pLog.logDebug("Attempting connection to server...")
	dbConnection = database.Database()
	if not dbConnection.connect("testDB", "testUser", "testPassword"):
		pLog.logError("Connection failed! Aborting test!")
		return
	
	#Test creating a table.
	testTableName = "TestTable"
	pLog.logDebug("Testing createTable()...")
	testSchema = Schema(testTableName, (
					("Id", Types.int, (Modifiers.primaryKey,)),
					("VarCharColumn", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
					("BoolColumn", Types.bool, ())
					))
	if not dbConnection.createTable(testSchema):
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
	listener = consoleListener.ConsoleListener()
	listener.setLogLevel(LogLevel.Verbose)
	mLog.attach(listener)
	testAll(mLog)
	mLog.shutdown()