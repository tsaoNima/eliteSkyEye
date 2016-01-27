'''
Created on Jan 19, 2016

@author: Me
'''
kTableProblem = 0x00
kColumnProblem = 0x10
kElementMissing = 0x01
kElementDoesNotMatchSpec = 0x02

class VerifyProblem(object):
	def __init__(self, pProblemCode, pProblemString):
		self.problemCode = pProblemCode
		self.problemString = pProblemString
		
	def __str__(self):
		return self.problemString
	
	__repr__ = __str__

#Actual definition of problems.
class TableMissing(VerifyProblem):
	def __init__(self, tableName):
		problemCode = kTableProblem | kElementMissing
		problemString = "Table {0} doesn't exist.".format(tableName)
		super(TableMissing, self).__init__(problemCode, problemString)

class TableSchemaMismatch(VerifyProblem):
	def __init__(self, tableName):
		problemCode = kTableProblem | kElementDoesNotMatchSpec
		problemString = "Table {0}'s schema doesn't match SkyEye's expected schema.".format(tableName)
		super(TableSchemaMismatch, self).__init__(problemCode, problemString)

class ColumnMissing(VerifyProblem):
	def __init__(self, tableName, columnName):
		problemCode = kColumnProblem | kElementMissing
		problemString = "Column {0} doesn't exist.".format(tableName + "." + columnName)
		super(ColumnMissing, self).__init__(problemCode, problemString)

class ColumnSchemaMismatch(VerifyProblem):
	def __init__(self, tableName, columnName, expectedSchema, actualSchema):
		problemCode = kColumnProblem | kElementDoesNotMatchSpec
		problemString = ("Column {0} doesn't match expected schema."
									"\n\tExpected column value: \"{1}\""
									"\n\tActual column value: \"{2}\"").format(tableName + "." + columnName,
																		 expectedSchema,
																		  actualSchema)
		super(ColumnSchemaMismatch, self).__init__(problemCode, problemString)
		
class ColumnConstraintMissing(VerifyProblem):
	def __init__(self, tableName, columnName, constraintType):
		problemCode = kColumnProblem | kElementMissing
		problemString = "Constraint {0} on column {1} doesn't exist.".format(constraintType, tableName + "." + columnName, tableName)
		super(ColumnConstraintMissing, self).__init__(problemCode, problemString)

class ColumnConstraintSchemaMismatch(VerifyProblem):
	def __init__(self, tableName, columnName, constraintType, expectedSchema, actualSchema):
		problemCode = kColumnProblem | kElementDoesNotMatchSpec
		problemString = ("Constraint {0} on column {1} doesn't match expected schema."
									"\n\tExpected column value: \"{2}\""
									"\n\tActual column value: \"{3}\"").format(constraintType,
																			tableName + "." + columnName,
																			expectedSchema,
																			actualSchema)
		super(ColumnConstraintSchemaMismatch, self).__init__(problemCode, problemString)