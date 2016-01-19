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

def TestAll(pLog):
	pLog.LogDebug("Please make sure that the server has the following:\n"
				"\tDatabase: testDB\n"
				"\tUsername: testUser\n"
				"\tPassword: testPassword\n")
	
	#Try connecting to a database.
	pLog.LogDebug("Attempting connection to server...")
	dbConnection = database.Database()
	if not dbConnection.Connect("testDB", "testUser", "testPassword"):
		pLog.LogError("Connection failed! Aborting test!")
		return
	
	#Test creating a table.
	testTableName = "test_table"
	pLog.LogDebug("Testing CreateTable()...")
	testSchema = Schema(testTableName, (
					("id", Types.int, (Modifiers.primaryKey,)),
					("var_char_column", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
					("bool_column", Types.bool, ())
					))
	if not dbConnection.CreateTable(testSchema):
		pLog.LogError("Table creation failed, aborting!")
		return
	
	#Make sure TableExists() finds existing tables
	#and can't find nonexistent tables.
	pLog.LogDebug("Testing TableExists()...")
	if not dbConnection.TableExists(testTableName):
		pLog.LogError("Couldn't find test table \"{0}\"!".format(testTableName))
	nonExistentTableName = "shouldNotExist"
	if dbConnection.TableExists(nonExistentTableName):
		pLog.LogError("Found nonexistent table \"{0}\"!".format(nonExistentTableName))
	
	#Test describing a table.
	pLog.LogDebug("Testing DescribeTable()...")
	tableDesc = dbConnection.DescribeTable(testTableName)
	if not tableDesc:
		pLog.LogError("Couldn't describe table \"{0}\"!".format(testTableName))
	else:
		pLog.LogDebug("Description of table \"{0}\":\n{1}".format(testTableName, tableDesc))
	
	#Test creating a related table.
	pLog.LogDebug("Creating table with foreign key...")
	relatedTableName = "related_table"
	relatedSchema = Schema(relatedTableName,
						(
						("id", Types.int, (Modifiers.primaryKey,)),
						("test_table", Types.int, (Modifiers.notNull, (Modifiers.references, testSchema.schemaName))),
						("another_column", Types.float, ())
						))
	if not dbConnection.CreateTable(relatedSchema):
		pLog.LogError("Table w/ foreign key creation failed!")
	else:
		#Try to describe the table.
		tableDesc = dbConnection.DescribeTable(relatedTableName)
		pLog.LogDebug("Description of table \"{0}\":\n{1}".format(relatedTableName, tableDesc))
	
	#Test dropping a table.
	pLog.LogDebug("Testing dropTable()...")
	#dbConnection.dropTable(relatedTableName)
	#Make sure the table's actually gone.
	if dbConnection.TableExists(relatedTableName):
		pLog.LogError("Test table \"{0}\" was not successfully dropped!".format(relatedTableName))
		
	#Delete the other table too.
	#dbConnection.dropTable(testTableName)
	if dbConnection.TableExists(testTableName):
		pLog.LogError("Test table \"{0}\" was not successfully dropped!".format(testTableName))
		
	#Close our connection.
	pLog.LogDebug("Closing connection to server...")
	dbConnection.Close()
	
if __name__ == "__main__":
	mLog = log.GetLogInstance()
	listener = consoleListener.ConsoleListener()
	listener.SetLogLevel(LogLevel.Verbose)
	mLog.Attach(listener)
	TestAll(mLog)
	mLog.Shutdown()