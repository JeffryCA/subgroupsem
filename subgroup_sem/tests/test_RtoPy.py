import unittest
from rpy2.robjects import r, pandas2ri
from rpy2 import robjects
from rpy2.robjects.conversion import localconverter
import numpy as np
import pandas as pd
from subgroup_sem.tests.DataSets import get_artificial_data



class TestRtoPy(unittest.TestCase):

	def test_conncection(self):
		robjects.globalenv['vector'] = robjects.IntVector([1, 0, 1, 0, 1, 1, 1])
		self.assertEqual(list(robjects.r['vector']), [1, 0, 1, 0, 1, 1, 1])


	def test_convert_df(self):
		data = get_artificial_data()
		with localconverter(robjects.default_converter + pandas2ri.converter): 
			robjects.globalenv['d'] = robjects.conversion.py2rpy(data)
			data_R = robjects.conversion.rpy2py( robjects.r['d'] )
		self.assertTrue(data.equals(data))

	




if __name__ == '__main__':
    unittest.main()
