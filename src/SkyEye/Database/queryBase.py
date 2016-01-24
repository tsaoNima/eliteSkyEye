'''
Created on Jan 24, 2016

@author: Me
'''
import collections
from SkyEye.Exceptions.exceptions import InvalidParameterError

kQueryBase = "SELECT {0} FROM {1} WHERE {2}"
kVariableEquals = "{0} = %s"
kColumnSeparator = ", "

class Boolean:
	And = "AND"
	Or = "OR"

class VariableElement(object):
	def __init__(self, variableName, booleanOperator = Boolean.And, assignString = kVariableEquals):
		self.Name = variableName
		self.AssignString = assignString.format(self.Name)
		self.Boolean = booleanOperator
		self.FullString = self.Boolean + " " + self.AssignString

class ColumnElement(object):
	def __init__(self, columnName, elementIndex):
		self.Name = columnName
		self.Index = elementIndex

class Query(object):
	'''Generic class for SELECT FROM WHERE queries.
	'''
	
	def buildVariables(self, pVariables, pVariableElements):
		#Only one of these can be set, otherwise we don't know
		#which to build the final variable list from.
		bothNone = pVariables is None and pVariableElements is None
		bothSet = pVariables is not None and pVariableElements is not None 
		if bothNone or bothSet:
			raise InvalidParameterError()
		
		#If the variable string tuple is set,
		#assume all variables are assigned with = and are AND'd together.
		if pVariables is not None:
			for varName in pVariables:
				self.variables.append(VariableElement(varName, booleanOperator=Boolean.And))
				
		#Otherwise, just copy over the given variable elements.
		else:
			assert pVariableElements is not None
			for var in pVariableElements:
				self.variables.append(var)
	
	def buildQueryString(self):
		#Build columns...
		numColumns = len(self.columns)
		assert numColumns > 0
		colString = ""
		for index, columnKey in enumerate(self.columns):
			columnIndex = self.columns[columnKey]
			assert columnIndex == index
			colString += kColumnSeparator + columnKey
		#Now you need to remove the first ", ", though.
		colString = colString.split(kColumnSeparator, 1)[1]
		
		#Source table can be copied in as is.
		
		#Variables must be iterated over.
		numVariables = self.NumVariables()
		assert numVariables > 0
		varString = self.variables[0].AssignString
		for var in self.variables[1:]:
			varString += " " + var.FullString
		
		#Now format all fields.
		return kQueryBase.format(colString, self.sourceTable, varString)
	
	def __init__(self, columns, sourceTable, variables = None, variableElements = None):
		"""Initializer.
		Parameters:
			* columns: The columns to be selected, as a tuple of strings.
			* sourceTable: The table to be selected from as a string. Can be a subquery,
			* but must be fully evaluated first.
			* variables: The variables to be used, as a tuple of strings. If set,
			variableObjects must be None or an InvalidParameterError will be raised.
			* variableElements: The variables to be used, as a tuple of VariableElements.
			If set, variables must be None or an InvalidParameterError will be raised.
		Raises:
			* InvalidParameterError if variables and variableElements are both None or
			both are *not* None.
		"""
		
		self.columns = collections.OrderedDict()
		"""Any columns to be selected.
		"""
		#Map columns to their indices.
		for newIndex, col in enumerate(columns):
			self.columns[col] = newIndex
		
		self.sourceTable = sourceTable
		"""The table to be selected from. Can be a subquery,
		but the query must be built as a string first.
		"""
		
		self.variables = []
		"""A list of VariableElements.
		"""
		self.buildVariables(variables, variableElements)
		
		#Build the final query string.
		self.QueryString = self.buildQueryString()
		"""A parameterized SQL query that can be passed to Database.execute().
		Does not include values for its parameters; those must be passed separately.
		"""
		
	def IndexForColumn(self, columnName):
		return self.columns[columnName]
	
	def NumVariables(self):
		return len(self.variables)
	
	def GetVariable(self, variableIndex):
		return self.variables[variableIndex]
	
	def __repr__(self):
		return self.QueryString