'''
Created on Jan 26, 2016

@author: Me
'''
from SkyEye.Database.schemaBase import DatabaseDefinition
from SkyEye.Database.schemaBase import TableDefinition
from SkyEye.Database.schemaBase import Column
from SkyEye.Database.schemaBase import Types
from SkyEye.Database.schemaBase import Modifiers
from SkyEye.Database.schemaBase import kSchemaNameLenMax

class RDASchemas(DatabaseDefinition):
	"""Describes all RDA tables.
	"""
	def __init__(self):
		self.Name = "recon_data_analyzer"
		self.AllSchemas = [
						TableDefinition("event_types",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax))
											),
						TableDefinition("player_info",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("user_id", Types.int, ()),
											Column("elite_name", Types.varchar, (), kSchemaNameLenMax))
											),
						TableDefinition("events",
										(Column("id", Types.int, (Modifiers.primaryKey,)),
										Column("event_date", Types.timestamp, (Modifiers.notNull,)))
										)
						]