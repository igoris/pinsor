from utility import *
from pinsor.ioc import *
import unittest
import mox

class test_container(unittest.TestCase):
	
	def setUp(self):
		self.mocker = mox.Mox()
	
	def tearDown(self):
		self.mocker.VerifyAll()
					
