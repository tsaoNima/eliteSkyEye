'''
Created on Jan 27, 2016

@author: Me
'''
class Get(object):
	def __init__(self, pTableName, pColumnName, pValue):
		self.TableName = pTableName
		self.ColumnName = pColumnName
		self.Value = pValue

class TableDefault(object):
	def __init__(self, pName, pColumns):
		self.Name = pName
		self.Columns = pColumns

AllDefaults = [
			TableDefault("celestial_types",
			(("Planet", False),
			("Moon", False),	#Does Elite actually have this distinction?
			("Star", True))
			),	#TODO
			
			TableDefault("ring_types",
			(("None"),
			("Rocky"),
			("Icy"))
			),	#TODO
			
			TableDefault("celestial_relationships",
			(("Orbits"),
			("Is On Surface Of"))),	#TODO
			
			TableDefault("governments",
			(("None", False),
			("Anarchy", False))),	#TODO
			
			TableDefault("economies",
			(("None"))),	#TODO
			
			TableDefault("superpowers",
			(("None"),
			("Empire"),
			("Federation"),
			("Alliance"))),
			
			TableDefault("cz_intensities",
			(("Low"),
			("High"))),
			
			TableDefault("global_states",
			(("None"))),	#TODO
			
			TableDefault("system_states",
			(("None"))),	#TODO
			
			TableDefault("factions",
			(("None",
			Get("governments", "name", "None"),
			Get("superpowers", "name", "None"),
			Get("global_states", "name", "None"),
			Get("global_states", "name", "None"))))	#TODO
			]