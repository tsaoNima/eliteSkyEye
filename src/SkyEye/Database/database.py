'''
Created on Jan 15, 2016

@author: Me
'''
import psycopg2
from ..Logging import log
from ..Logging.structs import LogLevel
import constants
from ..Constants import stringConstants

sLog = log.getLogInstance()

'''
Represents a database connection.
'''
class Database(object):
	#PostgreSQL connection.
	connection = None
	#The cursor, the thing that you perform database operations on.
	cursor = None
	connected = False
	
	#Returns True if query was successful, False otherwise.
	#failMsg should be a format string where the last parameter is the error string.
	def execute(self, query, queryParams, failMsg, failMsgParams = ()):
		if not self.connected:
			sLog.log(constants.kFmtErrNotConnected.format(constants.kMethodExecute), LogLevel.Verbose)
			return False
		try:
			self.cursor.execute(query,
						queryParams)
		except psycopg2.Error as e:
			sLog.log(failMsg.format(failMsgParams + e.diag.message_primary), LogLevel.Error)
			#Rollback is implicit; quit now.
			return False
		return True 
	
	def executeOnTable(self, tableName, invalidTableMsg, query, queryParams, failMsg, failMsgParams = ()):
		#Sanity check.
		if not tableName:
			sLog.log(invalidTableMsg, LogLevel.Warning)
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
	
	#Throws away all current database references.
	def abort(self):
		self.cursor = None
		self.connection = None
		self.connected = False
	
	'''
	Constructor.
	'''
	def __init__(self):
		#Initialize values to defaults.
		self.abort()
	
	'''
	Attempts to connect to the requested database
	on this machine.
	'''
	def connect(self, pDatabase, pUser, pPassword):
		port = constants.kDefaultDatabasePort
		sLog.log(constants.kFmtConnectionAttempted.format(constants.kMethodConnect, pDatabase, port, pUser),
				LogLevel.Debug)
		try:
			#Open the connection.
			#We probably want an autocommit connection, no point being explicit.
			#Host is localhost and port is going to be 5432.
			self.connection = psycopg2.connect(database=pDatabase, user=pUser, password=pPassword)
			self.connection.autocommit = True
			#Now get a cursor to start operations.
			self.cursor = self.connection.cursor();
			self.connected = True
			sLog.log(constants.kFmtConnectionSucceeded.format(constants.kMethodConnect, pDatabase, port, pUser),
					LogLevel.Debug)
		except psycopg2.Error as e:
			#Something bad happened.
			sLog.log(constants.kFmtErrConnectionFailed.format(constants.kMethodConnect, e.diag.message_primary), LogLevel.Error)
			self.close()
			return
		
	'''
	Closes database connection.
	'''
	def close(self):
		if self.cursor is not None:
			self.cursor.close()
		if self.connection is not None:
			self.connection.close()
		self.abort()
	
	'''
	Returns True if the requested table exists,
	False otherwise.
	'''
	def tableExists(self, tableName):
		if self.executeOnTable(tableName,
							constants.kFmtErrBadTableName.format(constants.kMethodTableExists),
							constants.kQueryCheckTableExists,
							(tableName,),
							constants.kFmtErrTableExistsFailed,
							(constants.kMethodTableExists,)):
			return self.cursor.fetchone()
		return False
	
	'''
	Describes a given table.
	'''
	def describeTable(self, tableName):
		if self.executeOnTable(tableName,
							constants.kFmtErrBadTableName.format(constants.kMethodDescribeTable),
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
							constants.kFmtErrBadTableName.format(constants.kMethodDropTable),
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
			sLog.log(constants.kFmtErrBadTableName.format(constants.kMethodCreateTable), LogLevel.Warning)
			return
		
		#Build the CREATE TABLE string.
		columns = self.buildColumnString(schema)
		
		#Do our query!
		createString = constants.kFmtQueryCreateTable.format(columns)
		self.execute(createString,
					(tableName,),
					constants.kFmtErrCreateTableFailed,
					(constants.kMethodCreateTable,))