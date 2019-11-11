#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 9 10:03 PM 2019

@author: Sushmith Ramesh

Test functions/classes from HW10_Sushmith_Ramesh.py using Python's unittest library
"""


import unittest
from HW10_Sushmith_Ramesh import UniversityRepository



class TestModuleGeneratorFile(unittest.TestCase):
    def test_UniversityRepository(self):
        """ Test whether the UniversityRepository class properly analyzes the 'students.txt', 
            'instructors.txt', 'grades.txt', and 'majors.txt' files in a specified directory 
            and prints them in pretty tables of a particular structure
        """
        majors_table = [('SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']), 
                        ('SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'])]

        student_table = [('10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None), 
                         ('10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None), 
                         ('10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], {'SSW 564', 'SSW 540'}, {'CS 501', 'CS 513', 'CS 545'}), 
                         ('10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, {'CS 501', 'CS 513', 'CS 545'}), 
                         ('10183', 'Chapman, O', 'SFEN', ['SSW 689'], {'SSW 567', 'SSW 564', 'SSW 555', 'SSW 540'}, {'CS 501', 'CS 513', 'CS 545'}), 
                         ('11399', 'Cordova, I', 'SYEN', ['SSW 540'], {'SYS 671', 'SYS 612', 'SYS 800'}, None), 
                         ('11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 671', 'SYS 612'}, {'SSW 565', 'SSW 540', 'SSW 810'}), 
                         ('11658', 'Kelly, P', 'SYEN', [], {'SYS 671', 'SYS 612', 'SYS 800'}, {'SSW 565', 'SSW 540', 'SSW 810'}), 
                         ('11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], {'SYS 671', 'SYS 612', 'SYS 800'}, {'SSW 565', 'SSW 540', 'SSW 810'}), 
                         ('11788', 'Fuller, E', 'SYEN', ['SSW 540'], {'SYS 671', 'SYS 612', 'SYS 800'}, None)]

        instructor_table = [('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4), 
                            ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3), 
                            ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3), 
                            ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3), 
                            ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1), 
                            ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1), 
                            ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1), 
                            ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1), 
                            ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1), 
                            ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1), 
                            ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2), 
                            ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)]

        Stevens = UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Py_Uni_Repo_Proj\Python_University_Repository")

        prog_majors_table = []
        for major in Stevens._majors_summary:
            prog_majors_table.append(tuple(major.pretty_print_major()))

        prog_student_table = []
        for student in Stevens._students_summary:
            prog_student_table.append(tuple(student.pretty_print_student()))

        prog_instructor_table = []
        for instructor in Stevens._instructors_summary:
            for info in instructor.pretty_print_instructor():
                prog_instructor_table.append(tuple(info))

        self.assertEqual(prog_majors_table, majors_table)
        self.assertEqual(prog_student_table, student_table)
        self.assertEqual(prog_instructor_table, instructor_table)

        with self.assertRaises(FileNotFoundError):
            UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Homework_11")



if __name__ == '__main__':
    """ predefined unit tests """
    unittest.main(exit=False, verbosity=2)
