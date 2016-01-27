'''
Created on Jan 26, 2016

@author: Me
'''
from ..subsystemBase import SubsystemBase
from SkyEye.Logging import log
from dbDefinition import GDWSchemas

sLog = log.GetLogInstance()

class GeoWarehouse(SubsystemBase):
	"""Subsystem for the geographic data warehouse (GDW).
	"""

	def onStart(self):
		"""Called when Start() is called.
		Subclasses should override this.
		"""
		pass
	
	def onShutdown(self):
		"""Called when Shutdown() is called
		but before the database connection is closed.
		Subclasses should override this.
		"""
		pass
	
	def __init__(self):
		schema = GDWSchemas()
		super(GeoWarehouse, self).__init__(schema.Name, schema)