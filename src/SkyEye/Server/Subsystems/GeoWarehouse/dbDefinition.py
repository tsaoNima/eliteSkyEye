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
												(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
												Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax),
												Column("is_star", Types.Bool, (Modifiers.NotNull,)))
												),
						TableDefinition("ring_types",
											(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
											Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax))
											),
						TableDefinition("celestial_relationships",
														(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
														Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax))
														),
						TableDefinition("governments",
											(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
											Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax),
											Column("generates_police", Types.Bool, (Modifiers.NotNull,)))
											),
						TableDefinition("economies",
											(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
											Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax))
											),
						TableDefinition("superpowers",
											(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
											Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax))
											),
						TableDefinition("cz_intensities",
												(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
												Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax))
												),
						TableDefinition("global_states",
												(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
												Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax))
												),
						TableDefinition("system_states",
												(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
												Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax))
												),
						TableDefinition("factions",
										(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
										Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax),
										Column("government", Types.Int, (Modifiers.NotNull,), pForeignKey="governments"),
										Column("superpower", Types.Int, (Modifiers.NotNull,), pForeignKey="superpowers"),
										Column("current_global_state", Types.Int, (Modifiers.NotNull,), pForeignKey="global_states"),
										Column("pending_global_state", Types.Int, (Modifiers.NotNull,), pForeignKey="global_states")
										)),
						TableDefinition("systems",
										(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
										Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax),
										Column("coord_x", Types.Float),
										Column("coord_y", Types.Float),
										Column("coord_z", Types.Float),
										Column("owning_faction", Types.Int, (Modifiers.NotNull,), pForeignKey="factions")
										)),
						TableDefinition("system_celestials",
													(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
													Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax),
													Column("celestial_type", Types.Int, (Modifiers.NotNull,), pForeignKey="celestial_types"),
													Column("ring_type", Types.Int, (Modifiers.NotNull,), pForeignKey="ring_types"),
													Column("distance_from_entry_point", Types.Float))
													),
						TableDefinition("structures",
											(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
											Column("name", Types.VarChar, (Modifiers.NotNull,), kSchemaNameLenMax),
											Column("owning_faction", Types.Int, (Modifiers.NotNull,), pForeignKey="factions"),
											Column("economy", Types.Int, (Modifiers.NotNull,), pForeignKey="economies"),
											Column("celestial", Types.Int, (Modifiers.NotNull,), pForeignKey="system_celestials"),
											Column("distance_from_celestial", Types.Float),
											Column("celestial_relationship", Types.Int, (Modifiers.NotNull,), pForeignKey="celestial_relationships")
											)),
						TableDefinition("wars",
									(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
									Column("faction_1", Types.Int, (Modifiers.NotNull,), pForeignKey="factions"),
									Column("faction_2", Types.Int, (Modifiers.NotNull,), pForeignKey="factions"),
									Column("war_start", Types.Timestamp, (Modifiers.NotNull,)),
									Column("war_end", Types.Timestamp))
									),
						TableDefinition("conflict_zones",
												(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
												Column("celestial", Types.Int, (Modifiers.NotNull,), pForeignKey="system_celestials"),
												Column("distance_from_celestial", Types.Float,
												Column("intensity", Types.Int, (Modifiers.NotNull,), pForeignKey="cz_intensities"),
												Column("war", Types.Int, (Modifiers.NotNull,), pForeignKey="wars"),
												Column("faction_1_deployed_cap_ship", Types.Bool, (Modifiers.NotNull,)),
												Column("faction_2_deployed_cap_ship", Types.Bool, (Modifiers.NotNull,)),
												Column("is_visible", Types.Bool, (Modifiers.NotNull,)),
												Column("last_updated", Types.Timestamp, (Modifiers.NotNull,))))
												),
						TableDefinition("factions_in_system",
													(Column("id", Types.Int, (Modifiers.PrimaryKey,)),
													Column("factions", Types.Int, (Modifiers.NotNull,), pForeignKey="factions"),
													Column("influence", Types.Float, (Modifiers.NotNull,)),
													Column("current_system_state", Types.Int, (Modifiers.NotNull,), pForeignKey="system_states"),
													Column("pending_system_state", Types.Int, (Modifiers.NotNull,), pForeignKey="system_states"),
													Column("entered_system_date", Types.Timestamp),
													Column("left_system_date", Types.Timestamp),
													Column("last_updated_date", Types.Timestamp, (Modifiers.NotNull,))
													))
						]