#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 3 7:03 PM 2019

@author: Sushmith Ramesh

Test functions/classes from HW09_Sushmith_Ramesh.py using Python's unittest library
"""


import unittest
from HW09_Sushmith_Ramesh import UniversityRepository



class TestModuleGeneratorFile(unittest.TestCase):
    def test_UniversityRepository(self):
        """ Test whether the UniversityRepository class properly analyzes the 'students.txt', 
            'instructors.txt', and 'grades.txt' files in a specified directory (information is 
            stored as nested dictionary)
        """
        file1 = UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Homework_9")
        self.assertEqual(dict(file1.students_summary[10103]), {('Baldwin', 'C'): ['SFEN']})
        self.assertEqual(dict(file1.instructors_summary[98764]), {('Feynman', 'R'): ['SFEN']})
        self.assertEqual(dict(file1.grades_summary[('SSW', '567')]), {98765: [10103, 10115, 10172, 10175]})
        self.assertNotEqual(dict(file1.instructors_summary[98762]), {('Feynman', 'R'): ['SFEN']})
        self.assertNotEqual(dict(file1.grades_summary[('SSW', '555')]), {98765: [10103, 10115, 10172, 10175]})

        with self.assertRaises(FileNotFoundError):
            UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Homework_10")

if __name__ == '__main__':
    """ predefined unit tests """
    unittest.main(exit=False, verbosity=2)
