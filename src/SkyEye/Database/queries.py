'''
Created on Jan 24, 2016

@author: Me
'''
from queryBase import Query
from queryBase import VariableElement

kVarLikeValue = "LOWER({0}) LIKE %s"

kQueryGetTableDatatypeInfo = Query(
								("column_name",
								"data_type",
								"character_maximum_length",
								"datetime_precision",
								"is_nullable"),
								"information_schema.columns",
								variables=("table_name",)
								) 
kQueryGetTablePrimaryOrUniqueInfo = Query(
										("constraint_name",
										"constraint_type"),
										"information_schema.table_constraints",
										variables=("table_name",)
										)
kQueryGetTableForeignInfo = Query(
							("constraint_name", "unique_constraint_name", "update_rule", "delete_rule"),
							"information_schema.referential_constraints",
							variableElements=(VariableElement("constraint_name", assignString=kVarLikeValue),)
							)