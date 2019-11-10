#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 3 7:03 PM 2019

@author: Sushmith Ramesh

Implement a class that stores information about students, instructors, classes, and grades for
a University (unfortunately, I read the hint after implementing all of the below...)
"""


import os
from collections import defaultdict
from prettytable import PrettyTable



class UniversityRepository:
    """ Analyze the 'students.txt', 'instructors.txt', and 'grades.txt' files in a specified 
        directory (information is stored as nested dictionary) and print out the details in a 
        pretty table

        Dictionaries Structure
        -----------------------
        students_summary: {id: {(last, first_initial): major}}
        instructors_summary: {id: {(last, first_initial): major}}
        grades_summary: {(class_major, class_number): {instructor_id: [student_id1, student_id2, ...]}}
        -----------------------
    """
    def __init__(self, directory):
        """ Set the directory path, initialize the students, instructors, and grades summaries 
            as three separate empty dictionaries, and call the analyze_files function to populate 
            all three ditionaries accordingly 
        """
        self.directory = directory
        self.students_summary = defaultdict(lambda: defaultdict(list))
        self.instructors_summary = defaultdict(lambda: defaultdict(list))
        self.grades_summary = defaultdict(lambda: defaultdict(list))

        self.analyze_files()

    def analyze_files(self):
        """ Store the information regarding students (id, name, and major), instructors (id, name, 
            and major), classes, and grades in the appropriate dictionaries created in __init__()
        """
        try:
            os.chdir(self.directory)
        except FileNotFoundError:
            raise FileNotFoundError(f"Directory {self.directory} was not found")

        students_path = os.path.join(self.directory, "students.txt")
        instructors_path = os.path.join(self.directory, "instructors.txt")
        grades_path = os.path.join(self.directory, "grades.txt")

        for student_info in self.file_reading_gen(students_path, 3, sep="\t"):
            self.students_summary[int(student_info[0])][tuple(student_info[1].split(", "))].append(student_info[2])

        for instructor_info in self.file_reading_gen(instructors_path, 3, sep="\t"):
            self.instructors_summary[int(instructor_info[0])][tuple(instructor_info[1].split(", "))].append(instructor_info[2])

        for grade_info in self.file_reading_gen(grades_path, 4, sep="\t"):
            self.grades_summary[tuple(grade_info[1].split(" "))][int(grade_info[3])].append(int(grade_info[0]))

    def file_reading_gen(self, path, fields, sep=',', header=False):
        """ return a generator that yields the content of a file (line by line) after parsing 
            based on a separator and checking for the expected number of fields - each line is 
            returned as a tuple and the first line of the file is skipped if header is True 
        """
        try:
            fp = open(path, 'r', encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open '{path}' for reading")
        else:
            with fp:
                file_index = 1
                if header == True:
                    file_index = 2
                    next(fp)
                for line_num, line in enumerate(fp, file_index):
                    single_line = line.rstrip('\n').split(sep)
                    single_line_len = len(single_line)
                    if single_line_len != fields:
                        raise ValueError(f"{path} has {single_line_len} field(s) on line {line_num} but expected {fields}")
                    else:
                        yield tuple(single_line)

    def pretty_print_student(self):
        """ Print/return a table that lists each student's CWID, name, and list of completed courses """
        pt = PrettyTable(field_names=["CWID", "Name", "Completed Course(s)"])
        for cwid in self.students_summary:
            class_list = sorted([' '.join(k) for k, v in self.grades_summary.items() if cwid in list(v.values())[0]])
            pt.add_row([cwid, ','.join(list(self.students_summary[cwid].keys())[0]), class_list])

        print(pt)
        # return pt

    def pretty_print_instructor(self):
        """ Print/return a table that lists instructor's CWID, name, department, list of courses taught, 
            and total number of students across all courses taught given that they teach at least one course
        """
        pt = PrettyTable(field_names=["CWID", "Name", "Dept", "Course(s)", "Student(s)"])
        for cwid in self.instructors_summary:
            class_list = list()
            students_per_class = list()
            for k, v in self.grades_summary.items():
                if cwid == list(v.keys())[0]:
                    class_list.append(' '.join(k))
                    students_per_class.append(len(list(v.values())[0]))

            instructor_name = list(self.instructors_summary[cwid].keys())[0]
            if class_list:
                pt.add_row([cwid, ','.join(instructor_name), self.instructors_summary[cwid][instructor_name][0], class_list, sum(students_per_class)])

        print(pt)
        # return pt



if __name__ == '__main__':
    """ main routine to run whole program """
    # file1 = UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Homework_9")

    # print("\nStudent Table:")
    # file1.pretty_print_student()

    # print("\nInstructor Table")
    # file1.pretty_print_instructor()
