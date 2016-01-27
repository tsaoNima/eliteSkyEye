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
												(Column("id", Types.Int, (Modifiers.primaryKey,)),
												Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax),
												Column("is_star", Types.Bool, (Modifiers.notNull,)))
												),
						TableDefinition("ring_types",
											(Column("id", Types.Int, (Modifiers.primaryKey,)),
											Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax))
											),
						TableDefinition("celestial_relationships",
														(Column("id", Types.Int, (Modifiers.primaryKey,)),
														Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax))
														),
						TableDefinition("governments",
											(Column("id", Types.Int, (Modifiers.primaryKey,)),
											Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax),
											Column("generates_police", Types.Bool, (Modifiers.notNull,)))
											),
						TableDefinition("economies",
											(Column("id", Types.Int, (Modifiers.primaryKey,)),
											Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax))
											),
						TableDefinition("superpowers",
											(Column("id", Types.Int, (Modifiers.primaryKey,)),
											Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax))
											),
						TableDefinition("cz_intensities",
												(Column("id", Types.Int, (Modifiers.primaryKey,)),
												Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax))
												),
						TableDefinition("global_states",
												(Column("id", Types.Int, (Modifiers.primaryKey,)),
												Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax))
												),
						TableDefinition("system_states",
												(Column("id", Types.Int, (Modifiers.primaryKey,)),
												Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax))
												),
						TableDefinition("factions",
										(Column("id", Types.Int, (Modifiers.primaryKey,)),
										Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax),
										Column("government", Types.Int, (Modifiers.notNull,), pForeignKey="governments"),
										Column("superpower", Types.Int, (Modifiers.notNull,), pForeignKey="superpowers"),
										Column("current_global_state", Types.Int, (Modifiers.notNull,), pForeignKey="global_states"),
										Column("pending_global_state", Types.Int, (Modifiers.notNull,), pForeignKey="global_states")
										)),
						TableDefinition("systems",
										(Column("id", Types.Int, (Modifiers.primaryKey,)),
										Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax),
										Column("coord_x", Types.Float),
										Column("coord_y", Types.Float),
										Column("coord_z", Types.Float),
										Column("owning_faction", Types.Int, (Modifiers.notNull,), pForeignKey="factions")
										)),
						TableDefinition("system_celestials",
													(Column("id", Types.Int, (Modifiers.primaryKey,)),
													Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax),
													Column("celestial_type", Types.Int, (Modifiers.notNull,), pForeignKey="celestial_types"),
													Column("ring_type", Types.Int, (Modifiers.notNull,), pForeignKey="ring_types"),
													Column("distance_from_entry_point", Types.Float))
													),
						TableDefinition("structures",
											(Column("id", Types.Int, (Modifiers.primaryKey,)),
											Column("name", Types.VarChar, (Modifiers.notNull,), kSchemaNameLenMax),
											Column("owning_faction", Types.Int, (Modifiers.notNull,), pForeignKey="factions"),
											Column("economy", Types.Int, (Modifiers.notNull,), pForeignKey="economies"),
											Column("celestial", Types.Int, (Modifiers.notNull,), pForeignKey="system_celestials"),
											Column("distance_from_celestial", Types.Float),
											Column("celestial_relationship", Types.Int, (Modifiers.notNull,), pForeignKey="celestial_relationships")
											)),
						TableDefinition("wars",
									(Column("id", Types.Int, (Modifiers.primaryKey,)),
									Column("faction_1", Types.Int, (Modifiers.notNull,), pForeignKey="factions"),
									Column("faction_2", Types.Int, (Modifiers.notNull,), pForeignKey="factions"),
									Column("war_start", Types.Timestamp, (Modifiers.notNull,)),
									Column("war_end", Types.Timestamp))
									),
						TableDefinition("conflict_zones",
												(Column("id", Types.Int, (Modifiers.primaryKey,)),
												Column("celestial", Types.Int, (Modifiers.notNull,), pForeignKey="system_celestials"),
												Column("distance_from_celestial", Types.Float,
												Column("intensity", Types.Int, (Modifiers.notNull,), pForeignKey="cz_intensities"),
												Column("war", Types.Int, (Modifiers.notNull,), pForeignKey="wars"),
												Column("faction_1_deployed_cap_ship", Types.Bool, (Modifiers.notNull,)),
												Column("faction_2_deployed_cap_ship", Types.Bool, (Modifiers.notNull,)),
												Column("is_visible", Types.Bool, (Modifiers.notNull,)),
												Column("last_updated", Types.Timestamp, (Modifiers.notNull,))))
												),
						TableDefinition("factions_in_system",
													(Column("id", Types.Int, (Modifiers.primaryKey,)),
													Column("factions", Types.Int, (Modifiers.notNull,), pForeignKey="factions"),
													Column("influence", Types.Float, (Modifiers.notNull,)),
													Column("current_system_state", Types.Int, (Modifiers.notNull,), pForeignKey="system_states"),
													Column("pending_system_state", Types.Int, (Modifiers.notNull,), pForeignKey="system_states"),
													Column("entered_system_date", Types.Timestamp),
													Column("left_system_date", Types.Timestamp),
													Column("last_updated_date", Types.Timestamp, (Modifiers.notNull,))
													))
						]