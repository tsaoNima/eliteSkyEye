'''
Created on Jan 27, 2016

@author: Me
'''
class Get(object):
	def __init__(self, pTableName, pColumnName, pValue):
		self.TableName = pTableName
		self.ColumnName = pColumnName
		self.Value = pValue

class DefaultRow(object):
	def __init__(self, pName, pColumns):
		self.Name = pName
		self.Columns = pColumns

class TableDefault(object):
	def __init__(self, pName, pRows):
		self.Name = pName
		self.Rows = pRows
		self.lookup = {}
		#Build lookup table for rows.
		for row in self.Rows:
			self.lookup[row.Name] = row
			
	def getRow(self, rowName):
		if not rowName in self.lookup.keys():
			return None
		else:
			return self.lookup[rowName]

class DatabaseDefault(object):
	def __init__(self, pName, pTables):
		self.Name = pName
		self.Tables = pTables
		self.lookup = {}
		#Build lookup table for tables.
		for table in self.Tables:
			self.lookup[table.Name] = table
			
	def getTable(self, tableName):
		if not tableName in self.lookup.keys():
			return None
		else:
			return self.lookup[tableName]
		
	def rowForKey(self, rowPath):
		"""Paths should be in the format "[table name].[row name]".
		"""
		splitPath = rowPath.split(".")
		table = self.getTable(splitPath[0])
		if table is None:
			return None
		else:
			row = table.getRow(splitPath[1])
			return row

AllDefaults = [
			TableDefault("celestial_types",
			(DefaultRow("planet", ("Planet", False)),
			DefaultRow("moon", ("Moon", False)),	#Does Elite actually have this distinction?
			DefaultRow("star", ("Star", True)))
			),	#TODO
			
			TableDefault("ring_types",
			(DefaultRow("none", ("None")),
			DefaultRow("rocky", ("Rocky")),
			DefaultRow("icy", ("Icy")))
			),	#TODO
			
			TableDefault("celestial_relationships",
			(DefaultRow("orbits", ("Orbits")),
			DefaultRow("on_surface", ("Is On Surface Of")))),	#TODO
			
			TableDefault("governments",
			(DefaultRow("none", ("None", False)),
			DefaultRow("anarchy", ("Anarchy", False)))),	#TODO
			
			TableDefault("economies",
			(DefaultRow("none", ("None")))),	#TODO
			
			TableDefault("superpowers",
			(DefaultRow("none", ("None")),
			DefaultRow("empire", ("Empire")),
			DefaultRow("federation", ("Federation")),
			DefaultRow("alliance", ("Alliance")))),
			
			TableDefault("cz_intensities",
			(DefaultRow("low", ("Low")),
			DefaultRow("high", ("High")))),
			
			TableDefault("global_states",
			(DefaultRow("none", ("None")))),	#TODO
			
			TableDefault("system_states",
			(DefaultRow("none", ("None")))),	#TODO
			
			TableDefault("factions",
			(DefaultRow("none", ("None",
			Get("governments", "name", "None"),
			Get("superpowers", "name", "None"),
			Get("global_states", "name", "None"),
			Get("global_states", "name", "None"))))),	#TODO
			
			#TODO: Add a data source metatable. Values should include:
			#	* None
			#	* SkyEye Server
			#	* SkyEye User
			#	* EDDB
			#	* INARA
			pass
			]