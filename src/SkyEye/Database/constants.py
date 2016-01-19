'''
Created on Jan 16, 2016

@author: Me
'''

kSchemaNameLenMax = 255
kDefaultDatabasePort = 5432

kGDWDatabaseName = "GeoDataWarehouse"
kRDADatabaseName = "ReconDataAnalyzer"

#Method names...
kMethodExecute = "Database.execute()"
kMethodConnect = "Database.connect()"
kMethodTableExists = "Database.tableExists()"
kMethodDescribeTable = "Database.describeTable()"
kMethodDropTable = "Database.dropTable()"
kMethodCreateTable = "Database.createTable()"
kMethodVerifyGDW = "Database.verifyGDW()"
kMethodVerifyRDA = "Database.verifyRDA()"

#Log strings...
kFmtErrNotConnected = "{0}: Not connected to database, aborting"
kFmtConnectionAttempted = "{0}: Connecting to {1}:{2} as {3}..."
kFmtConnectionSucceeded = "{0}: Connection to {1}:{2} as {3} successful."
kFmtErrConnectionFailed = "{0}: Connection failed with error: {1}"
kFmtErrBadTableName = "{0}: invalid table name passed, aborting"
kFmtErrDropTableFailed = "{0}: Table drop failed with error: {1}"
kFmtErrCreateTableFailed = "{0}: Table create failed with error: {1}"
kFmtErrTableExistsFailed = "{0}: Table existence check failed with error: {1}"
kFmtErrDescribeTableFailed = "Database.describeTable(): Table description failed with error: {0}"
kFmtWarnVerificationFailed = "Database.verifyAll(): {0} failed verification!"
kVerificationAllPassed = "Database.verifyAll(): All modules passed verification."
kFmtWarnSchemaFailed = "{0}: Schema {1} failed verification!"

#Queries...
#Describes the requested table.
#0: Table name.
kQueryDescribeTable = ("SELECT column_name, data_type, character_maximum_length, is_nullable "  
"FROM information_schema.columns WHERE table_name = %s;")
#Returns true if the requested table exists, false otherwise.
#Note that this doesn't check the current schema!
#0: Table name.
kQueryCheckTableExists = ("SELECT EXISTS (SELECT * FROM information_schema.tables "
						"WHERE table_name = %s);")
#Drops the requested table.
#0: Table name.
kQueryDropTable = "DROP TABLE \"{0}\";"
#Creates the requested table.
#0: Table name.
#1: Column info. Should be prebuilt and filled in with the formatter.
kFmtQueryCreateTable = "CREATE TABLE {0} ({1});"
#0: Column name.
#1: Column type.
#2: Column precision, if any.
#3: Column constraints, if any.
kFmtCreateColumn = "{0} {1}{2}{3}"
kSchemaColumnMinElems = 3
kSchemaColumnNameIdx = 0
kSchemaColumnTypeIdx = 1
kSchemaColumnConstraintIdx = 2
kSchemaColumnPrecisionIdx = 3
#0: The column's precision. If there is no precision,
#use an empty string instead of this constant.
kFmtColumnPrecision = "({0})"
#0: The column's constraints. If there are no constraints,
#use an empty string instead of this constant.
kFmtColumnConstraints = " {0}"
kConstraintSeparator = " "
kCreateColumnSeparator = ", "