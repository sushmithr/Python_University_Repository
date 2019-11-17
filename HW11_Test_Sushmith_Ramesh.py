#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:20 AM 2019

@author: Sushmith Ramesh

Test functions/classes from HW10_Sushmith_Ramesh.py using Python's unittest library
"""


import unittest
from HW11_Sushmith_Ramesh import UniversityRepository



class TestModuleGeneratorFile(unittest.TestCase):
    def test_UniversityRepository(self):
        """ Test whether the UniversityRepository class properly analyzes the 'students.txt', 
            'instructors.txt', 'grades.txt', and 'majors.txt' files in a specified directory 
            and prints them in pretty tables of a particular structure
        """
        majors_table = [('SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']), 
                        ('CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810'])]

        student_table = [('10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], {'SSW 540', 'SSW 555'}, None), 
                         ('10115', 'Bezos, J', 'SFEN', ['SSW 810'], {'SSW 540', 'SSW 555'}, {'CS 501', 'CS 546'}), 
                         ('10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], {'SSW 540'}, {'CS 501', 'CS 546'}), 
                         ('11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], None, None), 
                         ('11717', 'Kernighan, B', 'CS', [], {'CS 546', 'CS 570'}, {'SSW 565', 'SSW 810'})]

        instructor_table = [('98764', 'Cohen, R', 'SFEN', 'CS 546', 1), 
                            ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4), 
                            ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1), 
                            ('98762', 'Hawking, S', 'CS', 'CS 501', 1), 
                            ('98762', 'Hawking, S', 'CS', 'CS 546', 1), 
                            ('98762', 'Hawking, S', 'CS', 'CS 570', 1)]

        instructor_table_db = [('98762', 'Hawking, S', 'CS', 'CS 501', 1), 
                               ('98762', 'Hawking, S', 'CS', 'CS 546', 1), 
                               ('98762', 'Hawking, S', 'CS', 'CS 570', 1), 
                               ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1), 
                               ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4), 
                               ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1)]

        Stevens = UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Py_Uni_Repo_Proj\Python_University_Repository", r"C:\Sushmith Ramesh\SSW_810_Python\Py_Uni_Repo_Proj\Python_University_Repository\810_startup.db")

        prog_majors_table = [tuple(major.pretty_print_major()) for major in Stevens._majors_summary.values()]

        prog_student_table = [tuple(student.pretty_print_student()) for student in Stevens._students_summary.values()]

        prog_instructor_table = [tuple(info) for instructor in Stevens._instructors_summary.values() for info in instructor.pretty_print_instructor()]

        prog_instructor_table_db = Stevens._pretty_print_instructor_table_db(r"C:\Sushmith Ramesh\SSW_810_Python\Py_Uni_Repo_Proj\Python_University_Repository\810_startup.db")

        self.assertEqual(prog_majors_table, majors_table)
        self.assertEqual(prog_student_table, student_table)
        self.assertEqual(prog_instructor_table, instructor_table)
        self.assertEqual(prog_instructor_table_db, instructor_table_db)

        with self.assertRaises(FileNotFoundError):
            UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Homework_12", r"C:\Sushmith Ramesh\SSW_810_Python\Py_Uni_Repo_Proj\Python_University_Repository\810_startup.db")

        with self.assertRaises(FileNotFoundError):
            UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Homework_11", r"C:\Sushmith Ramesh\SSW_810_Python\Py_Uni_Repo_Proj\Python_University_Repository\910_startup.db")



if __name__ == '__main__':
    """ predefined unit tests """
    unittest.main(exit=False, verbosity=2)
