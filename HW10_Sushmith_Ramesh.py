#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 9 10:03 PM 2019

@author: Sushmith Ramesh

Implement a class that stores information about students, instructors, classes, grades, and 
majors for a University 

Potential Improvements:
1. Might be better to store students, instructors, and majors in defaultdict rather than 
    lists (too many nested for loops and possibility for duplicates in the 4 .txt files)
"""


import os
from collections import defaultdict
from prettytable import PrettyTable


def file_reading_gen(path, fields, sep=',', header=False):
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



class UniversityRepository:
    """ Analyze the 'students.txt', 'instructors.txt', 'grades.txt', and majors.txt files in 
        a specified directory (information is stored in series of lists) and print out the 
        details in a pretty table

        Dictionaries Structure
        -----------------------
        majors_summary: list of Major objects
        students_summary: list of Student objects
        instructors_summary: list of Instructor object
        -----------------------
    """
    def __init__(self, directory):
        """ Set the directory path, change cwd to directory path, initialize the students, 
            instructors, and grades summaries as three separate empty lists, call the 
            analyze_majors(), analyze_students(), analyze_instructors(), analyze_grades() 
            functions to populate all three lists accordingly, and finally print the information 
            in three different pretty tables
        """
        self._directory = directory
        try:
            os.chdir(self._directory)
        except FileNotFoundError:
            raise FileNotFoundError(f"Directory {self._directory} was not found")

        self._majors_summary = list()
        self._students_summary = list()
        self._instructors_summary = list()

        self._analyze_majors()
        self._analyze_students()
        self._analyze_instructors()
        self._analyze_grades()

        self._pretty_print_majors_table()
        self._pretty_print_student_table()
        self._pretty_print_instructor_table()

    def _analyze_majors(self):
        """ Read and store the information regarding majors (name, flag (required or elective), 
            and course) into 'Major' objects (created from 'Major' class) and append to majors_summary 
            list created in __init__()
        """
        majors_path = os.path.join(self._directory, "majors.txt")

        for name, flag, course in file_reading_gen(majors_path, 3, sep="\t", header=True):
            for major in self._majors_summary:
                if major._name == name:
                    if flag == 'R':
                        major._required_courses.add(course)
                    elif flag == 'E':
                        major._elective_courses.add(course)
                    else:
                        raise ValueError(f"Unknown flag: {flag} for major: {name} and course: {course}!")

                    break
            else:
                major_info = Major(name)
                if flag == 'R':
                    major_info._required_courses.add(course)
                elif flag == 'E':
                    major_info._elective_courses.add(course)
                else:
                    raise ValueError(f"Unknown flag: {flag} for major: {name} and course: {course}!")

                self._majors_summary.append(major_info)

    def _analyze_students(self):
        """ Read and store the information regarding students (cwid, name, major) into 'Student' 
            objects (created from 'Student' class) and append to students_summary list created 
            in __init__()
        """
        students_path = os.path.join(self._directory, "students.txt")

        for cwid, name, major in file_reading_gen(students_path, 3, sep=";", header=True):
            for major_obj in self._majors_summary:
                if major == major_obj._name:
                    self._students_summary.append(Student(cwid, name, major_obj))
                    break
            else:
                raise ValueError(f"Major: {major} for student: {cwid} is not a valid major!")

    def _analyze_instructors(self):
        """ Read and store the information regarding instructors (cwid, name, dept) into 'Instructor' 
            objects (created from 'Instructor' class) and append to instructors_summary list created 
            in __init__()
        """
        instructors_path = os.path.join(self._directory, "instructors.txt")

        for cwid, name, dept in file_reading_gen(instructors_path, 3, sep="|", header=True):
            self._instructors_summary.append(Instructor(cwid, name, dept))

    def _analyze_grades(self):
        """ Store the information regarding courses (student cwid, course, grade, instructor cwid) 
            as a part of the objects in the students_summary and instructors_summary lists
        """
        grades_path = os.path.join(self._directory, "grades.txt")

        for student_cwid, course, grade, instructor_cwid in file_reading_gen(grades_path, 4, sep="|", header=True):
            for student in self._students_summary:
                if student_cwid == student._cwid:
                    student._courses[course] = grade
                    break
            else:
                raise ValueError(f"The student with cwid: {student_cwid} could not be found!")

            for instructor in self._instructors_summary:
                if instructor_cwid == instructor._cwid:
                    instructor._courses[course] += 1
                    break
            else:
                raise ValueError(f"The instuctor with cwid: {instructor_cwid} could not be found!")

    def _pretty_print_majors_table(self):
        """ Print/return a table that lists each major's dept, list of required courses for the 
            major, and list of elective courses for the major 
        """
        pt = PrettyTable(field_names=Major.pretty_print_majors_header)
        for major in self._majors_summary:
            pt.add_row(major.pretty_print_major())

        print(pt)
        # return pt

    def _pretty_print_student_table(self):
        """ Print/return a table that lists each student's CWID, name, major, list of completed 
            courses, list of remaining required courses for their major, and list of remaining 
            elective courses for their major 
        """
        pt = PrettyTable(field_names=Student.pretty_print_student_header)
        for student in self._students_summary:
            pt.add_row(student.pretty_print_student())

        print(pt)
        # return pt

    def _pretty_print_instructor_table(self):
        """ Print/return a table that lists each instructor's CWID, name, dept, course taught, 
            and number of students in that course
        """
        pt = PrettyTable(field_names=Instructor.pretty_print_instructor_header)
        for instructor in self._instructors_summary:
            for info in instructor.pretty_print_instructor():
                pt.add_row(info)

        print(pt)
        # return pt



class Major:
    """ Represents the basic structure of a major inculding the name of the major, set of required 
        courses for the major and set of elective courses for the major. Also includes a method to 
        return a row of the major pretty table (the row represents info about the particular instance 
        of the major - the structure of the row is given in the pretty_print_majors_header variable below) 
        and a method to compute the status of a student, which returns list of completed courses, set of 
        still required courses, and set of still required electives for that student.
    """
    pretty_print_majors_header = ["Dept", "Required", "Elective(s)"]
    def __init__(self, name):
        """ Set the name of the major, required set of courses for the major, and set of electives 
            for the major (student of a particular major must take at least one elective course for 
            that major)
        """
        self._name = name
        self._required_courses = set()
        self._elective_courses = set()

    def pretty_print_major(self):
        """ Return the structure of a row needed in the major pretty table """
        return [self._name, sorted(list(self._required_courses)), sorted(list(self._elective_courses))]

    def compute_status(self, course_grades):
        """ Computes the list of completed courses, set of still required courses, and set 
            of still required electives for a student of a particular major 
        """
        completed_courses = [course for course in course_grades if not course_grades[course] > 'C']
        required_courses = self._required_courses - set(completed_courses)
        required_electives = None

        if set(completed_courses).isdisjoint(self._elective_courses):
            required_electives = self._elective_courses

        return self._name, completed_courses, required_courses, required_electives



class Student:
    """ Represents the basic structure of a student inculding the cwid, name, major, and course grades 
        of the student. Also includes a method to return a row of the student pretty table (the row represents 
        info about the particular instance of the student - the structure of the row is given in the 
        pretty_print_student_header variable below).
    """
    pretty_print_student_header = ["CWID", "Name", "Major", "Completed Course(s)", "Remaining Required", "Remaining Electives"]
    def __init__(self, cwid, name, major: Major):
        """ Set cwid, name, major, and courses dictionary for a student, where the courses 
            dictionary has a key for the course id and a value for the grade for that course
        """
        self._cwid = cwid
        self._name = name
        self._major = major
        self._courses = dict()

    def pretty_print_student(self):
        """ Return the structure of a row needed in the student pretty table """
        major, completed_courses, required_courses, required_electives = self._major.compute_status(self._courses)

        return [self._cwid, self._name, major, sorted(completed_courses), required_courses, required_electives]



class Instructor:
    """ Represents the basic structure of an instructor inculding the cwid, name, and dept of the instructor 
        alongside the number of students in each of the courses taught by the instructor. Also includes a 
        method to return a row of the instructor pretty table (the row represents info about the particular 
        instance of the instructor - the structure of the row is given in the pretty_print_instructor_header 
        variable below).
    """
    pretty_print_instructor_header = ["CWID", "Name", "Dept", "Course", "Student(s)"]
    def __init__(self, cwid, name, dept):
        """ Set cwid, name, dept, and courses dictionary for an instructor, where the courses 
            dictionary has a key for the course id and a value for the number of students in that
            course
        """
        self._cwid = cwid
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int)

    def pretty_print_instructor(self):
        """ Return the structure of a row needed in the instructor pretty table """
        for course in self._courses:
            yield [self._cwid, self._name, self._dept, course, self._courses[course]]



if __name__ == '__main__':
    """ main routine to run whole program """
    try:
        UniversityRepository(r"C:\Sushmith Ramesh\SSW_810_Python\Py_Uni_Repo_Proj\Python_University_Repository")
    except ValueError as e:
        print(f"ERROR: \n{e}")
    except FileNotFoundError as e:
        print(f"ERROR: \n{e}")
