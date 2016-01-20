'''
Created on Jan 18, 2016

@author: Me
'''
import database
from ..Logging import log
from ..Logging.structs import LogLevel
from ..Logging import consoleListener
from SkyEye.Server.schemas import Types
from SkyEye.Server.schemas import Modifiers
from SkyEye.Server.schemas import Schema
import SkyEye.Server.constants

def TestAll(pLog):
	kMethodTestAll = "tests.TestAll()"
	pLog.LogDebug("Please make sure that the server has the following:\n"
				"\tDatabase: testDB\n"
				"\tUsername: testUser\n"
				"\tPassword: testPassword\n",
				where=kMethodTestAll)
	
	#Try connecting to a database.
	pLog.LogDebug("Attempting connection to server...", where=kMethodTestAll)
	dbConnection = database.Database()
	if not dbConnection.Connect("testDB", "testUser", "testPassword"):
		pLog.LogError("Connection failed! Aborting test!", where=kMethodTestAll)
		return
	
	#Test creating a table.
	testTableName = "test_table"
	pLog.LogDebug("Testing CreateTable()...", where=kMethodTestAll)
	testSchema = Schema(testTableName, (
					("id", Types.int, (Modifiers.primaryKey,)),
					("var_char_column", Types.varchar, (Modifiers.notNull,), SkyEye.Server.constants.kSchemaNameLenMax),
					("bool_column", Types.bool, ())
					))
	if not dbConnection.CreateTable(testSchema):
		pLog.LogError("Table creation failed, aborting!", where=kMethodTestAll)
		return
	
	#Make sure TableExists() finds existing tables
	#and can't find nonexistent tables.
	pLog.LogDebug("Testing TableExists()...", where=kMethodTestAll)
	if not dbConnection.TableExists(testTableName):
		pLog.LogError("Couldn't find test table \"{0}\"!".format(testTableName), where=kMethodTestAll)
	nonExistentTableName = "shouldNotExist"
	if dbConnection.TableExists(nonExistentTableName):
		pLog.LogError("Found nonexistent table \"{0}\"!".format(nonExistentTableName), where=kMethodTestAll)
	
	#Test describing a table.
	pLog.LogDebug("Testing DescribeTable()...", where=kMethodTestAll)
	tableDesc = dbConnection.DescribeTable(testTableName)
	if not tableDesc:
		pLog.LogError("Couldn't describe table \"{0}\"!".format(testTableName), where=kMethodTestAll)
	else:
		pLog.LogDebug("Description of table \"{0}\":\n{1}".format(testTableName, tableDesc), where=kMethodTestAll)
	
	#Test creating a related table.
	pLog.LogDebug("Creating table with foreign key...", where=kMethodTestAll)
	relatedTableName = "related_table"
	relatedSchema = Schema(relatedTableName,
						(
						("id", Types.int, (Modifiers.primaryKey,)),
						("test_table", Types.int, (Modifiers.notNull, (Modifiers.references, testSchema.schemaName))),
						("another_column", Types.float, ())
						))
	if not dbConnection.CreateTable(relatedSchema):
		pLog.LogError("Table w/ foreign key creation failed!", where=kMethodTestAll)
	else:
		#Try to describe the table.
		tableDesc = dbConnection.DescribeTable(relatedTableName)
		pLog.LogDebug("Description of table \"{0}\":\n{1}".format(relatedTableName, tableDesc), where=kMethodTestAll)
	
	#Test dropping a table.
	pLog.LogDebug("Testing dropTable()...")
	dbConnection.DropTable(relatedTableName)
	#Make sure the table's actually gone.
	if dbConnection.TableExists(relatedTableName):
		pLog.LogError("Test table \"{0}\" was not successfully dropped!".format(relatedTableName), where=kMethodTestAll)
		
	#Delete the other table too.
	dbConnection.DropTable(testTableName)
	if dbConnection.TableExists(testTableName):
		pLog.LogError("Test table \"{0}\" was not successfully dropped!".format(testTableName), where=kMethodTestAll)
		
	#Disconnect our connection.
	pLog.LogDebug("Closing connection to server...", where=kMethodTestAll)
	dbConnection.Disconnect()
	
if __name__ == "__main__":
	mLog = log.GetLogInstance()
	listener = consoleListener.ConsoleListener()
	listener.SetLogLevel(LogLevel.Verbose)
	mLog.Attach(listener)
	TestAll(mLog)
	mLog.Shutdown()