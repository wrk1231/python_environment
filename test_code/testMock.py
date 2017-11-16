#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xiaotie'
import sys
sys.path.append('..')
sys.path.append('../..')
from mock import patch
import unittest

class testClass():
    def testFun(self):
        a = self.add(1)
        b = self.add(2)
        print a,b

    def add(self, x):
        return x*2

class testMock(unittest.TestCase):
    def test1(self):
        testClass().testFun()

    @patch.object(testClass, "add")
    def test2(self, mock):
        mock.side_effect = [90,100]
        testClass().testFun()

if __name__ == '__main__':
    unittest.main()