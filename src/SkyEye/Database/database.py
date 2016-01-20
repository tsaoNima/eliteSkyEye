'''
Created on Jan 15, 2016

@author: Me
'''
import psycopg2
import constants
from ..Logging import log
from ..Logging.structs import LogLevel

sLog = log.GetLogInstance()

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
	def execute(self, callerName, query, queryParams, failMsg, failMsgParams = ()):
		if not self.connected:
			sLog.LogVerbose(constants.kErrNotConnected, constants.kTagDatabase, constants.kMethodExecute)
			return False
		try:
			self.cursor.execute(query,
						queryParams)
		except psycopg2.Error as e:
			allParams = failMsgParams + (e,)
			sLog.LogError(failMsg.format(*allParams), constants.kTagDatabase, callerName)
			self.connection.rollback()
			return False
		self.connection.commit()
		return True
	
	def executeOnTable(self, callerName, tableName, query, queryParams, failMsg, failMsgParams = ()):
		#Sanity check.
		if not tableName:
			sLog.LogWarning(constants.kFmtErrBadTableName.format(tableName), constants.kTagDatabase, constants.kMethodExecuteOnTable)
			return False
		
		return self.execute(callerName, query, queryParams, failMsg, failMsgParams)
	
	def buildConstraintString(self, constraint):
		result = ""
		#Is this constraint a string?
		if isinstance(constraint, basestring):
			#If it is, return without expanding.
			result = constraint
		else:
			#Otherwise, use subsequent elements as parameters.
			#In practice only REFERENCES has parameters, and for now it only refers to the table;
			#We don't FK on anything besides the referent's PK, so that's fine.
			assert len(constraint) > 1
			result = constraint[0] + " " + constraint[1]
		return result
	
	def buildSingleColumn(self, column):
		#Does this have precision?
		precisionStr = ""
		if len(column) > constants.kSchemaColumnMinElems:
			precisionStr = constants.kFmtColumnPrecision.format(column[constants.kSchemaColumnPrecisionIdx])
		#Does this have constraints?
		constraints = column[constants.kSchemaColumnConstraintIdx]
		constraintStr = ""
		#Build the constraint string, space separating each constraint.
		if len(constraints) > 0:
			constraintStr = self.buildConstraintString(constraints[0])
			for c in constraints[1:]:
				constraintStr += constants.kConstraintSeparator + self.buildConstraintString(c)
			#Convert that into the final constraint string.
			constraintStr = constants.kFmtColumnConstraints.format(constraintStr)
		#Now build our column.
		return constants.kFmtCreateColumn.format(column[constants.kSchemaColumnNameIdx],
													column[constants.kSchemaColumnTypeIdx],
													precisionStr,
													constraintStr)
	
	#Builds a column string based on the given schema.
	#Returns the column string.
	def buildColumnString(self, schema):
		if not schema:
			return ""
		#Generally a column goes:
		#"[name] [type]([precision]),"
		#Constrained columns have the format:
		#"[name] [type]([precision]) [constraints],"
		#Build the first column.
		result = self.buildSingleColumn(schema[0])
		for column in schema[1:]:
			result += constants.kCreateColumnSeparator + self.buildSingleColumn(column)
		return result
	
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
	
	def IsConnected(self):
		return self.connected
	
	'''
	Attempts to connect to the requested database
	on this machine.
	Returns True if the connection was successful, False otherwise.
	'''
	def Connect(self, pDatabase, pUser, pPassword):
		port = constants.kDefaultDatabasePort
		sLog.LogDebug(constants.kFmtConnectionAttempted.format(pDatabase, port, pUser),
				constants.kTagDatabase,
				constants.kMethodConnect)
		try:
			#Open the connection.
			#We probably want an autocommit connection, no point being explicit.
			#Host is localhost and port is going to be 5432.
			self.connection = psycopg2.connect(database=pDatabase, user=pUser, password=pPassword)
			#self.connection.autocommit = True
			#Now get a cursor to start operations.
			self.cursor = self.connection.cursor();
			self.connected = True
			sLog.LogDebug(constants.kFmtConnectionSucceeded.format(pDatabase, port, pUser),
					constants.kTagDatabase,
					constants.kMethodConnect)
			return True
		except psycopg2.Error as e:
			#Something bad happened.
			sLog.LogError(constants.kFmtErrConnectionFailed.format(e),
						constants.kTagDatabase,
						constants.kMethodConnect)
			self.Close()
			return False
		
	'''
	Closes database connection.
	'''
	def Close(self):
		if self.cursor is not None:
			self.cursor.close()
		if self.connection is not None:
			self.connection.close()
		self.abort()
	
	'''
	Returns True if the requested table exists,
	False otherwise.
	'''
	def TableExists(self, tableName):
		if self.executeOnTable(constants.kMethodTableExists,
							tableName,
							constants.kQueryCheckTableExists,
							(tableName,),
							constants.kFmtErrTableExistsFailed):
			return self.cursor.fetchone()[0]
		return False
	
	'''
	Describes a given table.
	Returns the table's schema if successful,
	or an empty tuple if the table could not be found for any reason.
	'''
	def DescribeTable(self, tableName):
		if self.executeOnTable(constants.kMethodDescribeTable,
							tableName,
							constants.kQueryDescribeTable,
							(tableName,),
							constants.kFmtErrDescribeTableFailed):
			return self.cursor.fetchall()
		return ()
	
	'''
	Attempts to drop the requested table.
	Returns True if the table was dropped, False otherwise.
	'''
	def DropTable(self, tableName):
		queryStr = constants.kQueryDropTable.format(tableName)
		sLog.LogWarning(constants.kFmtWarnDroppingTable.format(tableName),
					constants.kTagDatabase,
					constants.kMethodDropTable)
		return self.executeOnTable(constants.kMethodDropTable,
								tableName,
								queryStr,
								(),
								constants.kFmtErrDropTableFailed)
		
	'''
	Attempts to create the requested table with the given schema.
	Returns True if the table was created, False otherwise.
	'''
	def CreateTable(self, schema):
		#Sanity check.
		if not schema.schemaName:
			sLog.LogWarning(constants.kFmtErrBadTableName.format(schema.schemaName), constants.kTagDatabase, constants.kMethodCreateTable)
			return
		
		#Build the CREATE TABLE string.
		columns = self.buildColumnString(schema.schemaColumns)
		
		#Do our query!
		createString = constants.kFmtQueryCreateTable.format(schema.schemaName, columns)
		sLog.LogDebug(constants.kFmtCreatingTable.format(createString),
					constants.kTagDatabase,
					constants.kMethodCreateTable)
		return self.execute(constants.kMethodCreateTable,
						createString,
						(),
						constants.kFmtErrCreateTableFailed)