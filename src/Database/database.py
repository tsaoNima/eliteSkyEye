'''
Created on Jan 15, 2016

@author: Me
'''
import psycopg2
from Output import log
from Output.structs import LogLevel
from Database import constants

sLog = log.getLogInstance()

'''
classdocs
'''
class Database(object):
	#PostgreSQL connection.
	connection = None
	#The cursor, the thing that you perform database operations on.
	cursor = None
	
	#Returns True if query was successful, False otherwise.
	#failMsg should be a format string where the last parameter is the error string.
	def execute(self, query, queryParams, failMsg, failMsgParams = ()):
		try:
			self.cursor.execute(query,
						queryParams)
		except psycopg2.Error as e:
			sLog.log(failMsg % failMsgParams + e.diag.message_primary, LogLevel.Error)
			#Rollback is implicit; quit now.
			return False
		return True 
	
	def executeOnTable(self, tableName, tableNotFoundMsg, query, queryParams, failMsg, failMsgParams = ()):
		#Sanity check.
		if not tableName:
			sLog.log(tableNotFoundMsg, LogLevel.Warning)
			return False
		
		return self.execute(query, queryParams, failMsg, failMsgParams)
	
	#Builds a column string based on the given schema.
	#Returns the column string.
	def buildColumnString(self, schema):
		#Generally a column goes:
		#"[name] [type]([precision]),"
		#Constrained columns have the format:
		#"[name] [type]([precision]) [constraints],"
		pass
	
	'''
	Constructor.
	'''
	def __init__(self, params):
		#Initialize values to defaults.
		self.connection = None
		self.cursor = None
	
	'''
	Attempts to connect to the requested database
	on this machine.
	'''
	def connect(self, pDatabase, pUser, pPassword):
		try:
			#Open the connection.
			#We probably want an autocommit connection, no point being explicit.
			#Host is localhost and port is going to be 5432.
			self.connection = psycopg2.connect(database=pDatabase, user=pUser, password=pPassword)
			self.connection.autocommit = True
			#Now get a cursor to start operations.
			self.cursor = self.connection.cursor();
		except psycopg2.Error as e:
			#Something bad happened.
			sLog.log(constants.kFmtErrConnectionFailed % e.diag.message_primary, LogLevel.Error)
			self.connection = None
			self.cursor = None
			return
		
	'''
	Closes database connection.
	'''
	def close(self):
		self.cursor.close()
		self.connection.close()
	
	'''
	Describes a given table.
	'''
	def describeTable(self, tableName):
		if self.executeOnTable(tableName,
							constants.kFmtErrBadTableName % constants.kMethodDescribeTable,
							constants.kQueryDescribeTable,
							(tableName,),
							constants.kFmtErrDescribeTableFailed):
			return self.cursor.fetchall()
		return ()
	
	'''
	Attempts to drop the requested table.
	'''
	def dropTable(self, tableName):
		self.executeOnTable(tableName,
							constants.kFmtErrBadTableName % constants.kMethodDropTable,
							constants.kQueryDropTable,
							(tableName,),
							constants.kFmtErrDropTableFailed,
							(constants.kMethodDropTable,))
		
	'''
	Attempts to create the requested table with the given schema.
	'''
	def createTable(self, tableName, schema):
		#Sanity check.
		if not tableName:
			sLog.log(constants.kFmtErrBadTableName % constants.kMethodCreateTable, LogLevel.Warning)
			return
		
		#Build the CREATE TABLE string.
		columns = self.buildColumnString(schema)
		
		#Do our query!
		createString = constants.kFmtQueryCreateTable % columns
		self.execute(createString,
					(tableName,),
					constants.kFmtErrCreateTableFailed,
					(constants.kMethodCreateTable,))