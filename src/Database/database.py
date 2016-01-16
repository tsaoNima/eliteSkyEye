import psycopg2
from Output import log
from Output.structs import LogLevel
from Database import constants

'''
Created on Jan 15, 2016

@author: Me
'''

#Constants.
kFmtConnectionString = "dbname={0} user={1}"

sLog = log.getLogInstance()

'''
classdocs
'''
class Database(object):
	#PostgreSQL connection.
	connection = None
	#The cursor, the thing that you perform database operations on.
	cursor = None
	
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
		#Sanity check.
		if not tableName:
			sLog.log(constants.kFmtErrDescribeTableBadTableName, LogLevel.Warning)
			return
		
		#Otherwise, do our query!
		try:
			self.cursor.execute(constants.kFmtQueryDescribeTable,
						tableName)
		except psycopg2.Error as e:
			sLog.log(constants.kFmtErrDescribeTableFailed % e.diag.message_primary, LogLevel.Error)
			#Rollback is implicit; quit now.
			return ()
			
		return self.cursor.fetchall()