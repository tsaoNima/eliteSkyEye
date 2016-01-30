'''
Created on Jan 26, 2016

@author: Me
'''
from ..subsystemBase import SubsystemBase
from SkyEye.Logging import log
from dbDefinition import RDASchemas

sLog = log.GetLogInstance()

class ReconAnalyzer(SubsystemBase):
	"""Subsystem for the recon data analyzer (RDA).
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
		schema = RDASchemas()
		super(ReconAnalyzer, self).__init__(schema.Name, schema)