from utility import *
from ioc import *
import unittest
import mox

class container_tests(unittest.TestCase):
	
	def setUp(self):
		self.mocker = mox.Mox()
	
	def tearDown(self):
		self.mocker.VerifyAll()
					
