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

class GDWSchemas(DatabaseDefinition):
	"""Describes all GDW tables.
	"""
	
	def __init__(self):
		self.Name = "geo_data_warehouse"
		self.AllSchemas = [
						TableDefinition("celestial_types",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax),
												Column("is_star", Types.bool, (Modifiers.notNull,)))
												),
						TableDefinition("ring_types",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax))
											),
						TableDefinition("celestial_relationships",
														(Column("id", Types.int, (Modifiers.primaryKey,)),
														Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax))
														),
						TableDefinition("governments",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax),
											Column("generates_police", Types.bool, (Modifiers.notNull,)))
											),
						TableDefinition("economies",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax))
											),
						TableDefinition("superpowers",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax))
											),
						TableDefinition("cz_intensities",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax))
												),
						TableDefinition("global_states",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax))
												),
						TableDefinition("system_states",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax))
												),
						TableDefinition("factions",
										(Column("id", Types.int, (Modifiers.primaryKey,)),
										Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax),
										Column("government", Types.int, (Modifiers.notNull,), pForeignKey="governments"),
										Column("superpower", Types.int, (Modifiers.notNull,), pForeignKey="superpowers"),
										Column("current_global_state", Types.int, (Modifiers.notNull,), pForeignKey="global_states"),
										Column("pending_global_state", Types.int, (Modifiers.notNull,), pForeignKey="global_states")
										)),
						TableDefinition("systems",
										(Column("id", Types.int, (Modifiers.primaryKey,)),
										Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax),
										Column("coord_x", Types.float),
										Column("coord_y", Types.float),
										Column("coord_z", Types.float),
										Column("owning_faction", Types.int, (Modifiers.notNull,), pForeignKey="factions")
										)),
						TableDefinition("system_celestials",
													(Column("id", Types.int, (Modifiers.primaryKey,)),
													Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax),
													Column("celestial_type", Types.int, (Modifiers.notNull,), pForeignKey="celestial_types"),
													Column("ring_type", Types.int, (Modifiers.notNull,), pForeignKey="ring_types"),
													Column("distance_from_entry_point", Types.float))
													),
						TableDefinition("structures",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), kSchemaNameLenMax),
											Column("owning_faction", Types.int, (Modifiers.notNull,), pForeignKey="factions"),
											Column("economy", Types.int, (Modifiers.notNull,), pForeignKey="economies"),
											Column("celestial", Types.int, (Modifiers.notNull,), pForeignKey="system_celestials"),
											Column("distance_from_celestial", Types.float),
											Column("celestial_relationship", Types.int, (Modifiers.notNull,), pForeignKey="celestial_relationships")
											)),
						TableDefinition("wars",
									(Column("id", Types.int, (Modifiers.primaryKey,)),
									Column("faction_1", Types.int, (Modifiers.notNull,), pForeignKey="factions"),
									Column("faction_2", Types.int, (Modifiers.notNull,), pForeignKey="factions"),
									Column("war_start", Types.timestamp, (Modifiers.notNull,)),
									Column("war_end", Types.timestamp))
									),
						TableDefinition("conflict_zones",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("celestial", Types.int, (Modifiers.notNull,), pForeignKey="system_celestials"),
												Column("distance_from_celestial", Types.float,
												Column("intensity", Types.int, (Modifiers.notNull,), pForeignKey="cz_intensities"),
												Column("war", Types.int, (Modifiers.notNull,), pForeignKey="wars"),
												Column("faction_1_deployed_cap_ship", Types.bool, (Modifiers.notNull,)),
												Column("faction_2_deployed_cap_ship", Types.bool, (Modifiers.notNull,)),
												Column("is_visible", Types.bool, (Modifiers.notNull,)),
												Column("last_updated", Types.timestamp, (Modifiers.notNull,))))
												),
						TableDefinition("factions_in_system",
													(Column("id", Types.int, (Modifiers.primaryKey,)),
													Column("factions", Types.int, (Modifiers.notNull,), pForeignKey="factions"),
													Column("influence", Types.float, (Modifiers.notNull,)),
													Column("current_system_state", Types.int, (Modifiers.notNull,), pForeignKey="system_states"),
													Column("pending_system_state", Types.int, (Modifiers.notNull,), pForeignKey="system_states"),
													Column("entered_system_date", Types.timestamp),
													Column("left_system_date", Types.timestamp),
													Column("last_updated_date", Types.timestamp, (Modifiers.notNull,))
													))
						]