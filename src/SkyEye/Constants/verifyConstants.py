'''
Created on Jan 19, 2016

@author: Me
'''
kTableProblem = 0x00
kColumnProblem = 0x10
kElementMissing = 0x01
kElementDoesNotMatchSpec = 0x02

class VerifyProblem(object):
	problemCode = 0
	problemString = ""
	
	def __init__(self, pProblemCode, pProblemString):
		self.problemCode = pProblemCode
		self.problemString = pProblemString
		
	def __str__(self):
		return self.problemString
	
	__repr__ = __str__

#Actual definition of problems.
class TableMissing(VerifyProblem):
	def __init__(self, tableName):
		pCode = kTableProblem | kElementMissing
		pString = "Table {0} doesn't exist".format(tableName)
		super(TableMissing, self).__init__(pCode, pString)

class TableSchemaMismatch(VerifyProblem):
	def __init__(self, tableName):
		pCode = kTableProblem | kElementDoesNotMatchSpec
		pString = "Table {0}'s schema doesn't match SkyEye's expected schema".format(tableName)
		super(TableSchemaMismatch, self).__init__(pCode, pString)

class ColumnMissing(VerifyProblem):
	def __init__(self, tableName, columnName):
		pCode = kColumnProblem | kElementMissing
		pString = "Column {0} of table {1} does not exist".format(columnName, tableName)
		super(ColumnMissing, self).__init__(pCode, pString)

class ColumnSchemaMismatch(VerifyProblem):
	def __init__(self, columnName, expectedSchema, actualSchema):
		pCode = kColumnProblem | kElementDoesNotMatchSpec
		pString = ("Column {0} doesn't match expected schema.",
									"\n\tExpected column: \"{1}\"",
									"\n\tActual column: \"{2}\"").format(columnName,
																		 expectedSchema,
																		  actualSchema)
		super(ColumnSchemaMismatch, self).__init__(pCode, pString)