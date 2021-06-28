# Any changes to the distributions library should be reinstalled with
#  pip install --upgrade .

# For running unit tests, use
# /usr/bin/python -m unittest test
import numpy as np
import unittest

from mcsim import *

class TestNormal(unittest.TestCase):
    '''Tests for the pdf_normal function.'''
    def test_normal_value(self):
        # Test some values produced
        expected = [0.40, 0.06]
        tests = [pdf_normal(0), pdf_normal(1.96)]
        actual = [round(x, 2) for x in tests]
        self.assertEqual(actual, expected, 'Normal PDF values incorrect.')
    
    def test_sigma_positive(self):
        actual = pdf_normal(1, sigma=-1)
        expected = None
        self.assertEqual(actual, expected, 'Negative variance should not be allowed.')


class TestExponential(unittest.TestCase):
    '''Tests for the pdf_exponential function.'''
    def test_exponential_value(self):
        # Test some values produced
        expected = [0.30, 0.39]
        tests = [pdf_exponential(1), pdf_exponential(0.5)]
        actual = [round(x, 2) for x in tests]
        self.assertEqual(actual, expected, 'Exponential PDF values incorrect.')

    def test_positive_rate(self):
        # Test that lambda is positive
        expected = None
        actual = pdf_exponential(2, lam = -3)
        self.assertEqual(actual, expected, 'Rate parameter must be positive.')

    def test_positive_support(self):
        # Test for positive support
        expected = 0.0
        actual = float(pdf_exponential(-3))
        self.assertEqual(actual, expected, 'Exponential has only positive support.')


class TestUniform(unittest.TestCase):
    '''Tests for the pdf_uniform function'''
    def test_uniform_values(self):
        # Test some values produced
        expected = [0.5, 1.0]
        tests = [pdf_uniform(1, 0, 2), pdf_uniform(0.5)]
        actual = [round(x, 2) for x in tests]
        self.assertEqual(actual, expected, 'Uniform pdf values incorrect.')

    def test_bounds_dont_cross(self):
        # Test b > a
        expected = None
        actual = pdf_uniform(1, 2, 1)
        self.assertEqual(actual, expected, 'Lower bound exceeds upper bound.')

    def test_query_in_bounds(self):
        # Test for support in bounds
        expected = 0.0
        actual = pdf_uniform(2)
        self.assertEqual(actual, expected, 'Support should be in (a,b).')      

    
if __name__ == '__main__':
    unittest.main()