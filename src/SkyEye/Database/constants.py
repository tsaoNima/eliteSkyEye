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
kQueryDescribeTable = "select column_name, data_type, character_maximum_length, is_nullable "
"from INFORMATION_SCHEMA.COLUMNS where table_name = %s;"
kQueryCheckTableExists = "if exists (select * from information_schema.tables where table_name = %s) "
"select TRUE as result else select FALSE as result"
#Drops the requested table.
kQueryDropTable = "drop table %s;"
#Creates the requested table.
#Column info should be prebuilt and filled in with the formatter.
kFmtQueryCreateTable = "create table %s ({0});"
kFmtCreateWithPrecision = "{0}({1})"
kCreateColumnSeparator = ","