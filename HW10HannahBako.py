""" This program contains three classes that read data from files containing information about students and instructors
and then creates a repository of data."""
from prettytable import PrettyTable
from collections import defaultdict
import unittest


class Student:
    """This class represents the student object and contains the name, cwid, major and courses offered by the student"""
    def __init__(self, name = "john Doe", cwid = 0000, major ="Not assigned" ):
        self.name = name
        self.cwid = cwid
        self.major = major
        self.courses = defaultdict(str)

    def add_grades(self, grade, course):
        self.courses[course] = grade


class Instructor:
    """This class represents the instructor and contains the name, cwid, department, courses taught and number of students
    in each course"""
    def __init__(self, cwid, name, department):
        self.name = name
        self.cwid = cwid
        self.department = department
        self.courses = defaultdict(int)

    def add_courses(self, students, course):
        self.courses[course] = students


class Repo:
    """This class is the repository for the data it extracts the data from the files and performs the necessary operations"""
    dict_student = dict()
    dict_instructor = dict()
    def __init__(self):
        self.readstudent()
        self.readinstructor()
        self.readgrades()

    def add_student(self, cwid, student):
        self.dict_student[cwid] = student

    def add_Instructor(self, cwid, instructor):
        self.dict_instructor[cwid] = instructor

    def get_student(self, cwid):
       return self.dict_student[cwid]

    def get_instructo(self, cwid):
        return self.dict_instructor[cwid]

    def readstudent(self):
        """reads students data and creates student objects"""
        path = "/home/hannah/Documents/Schoolstuff/Books/sws810/College/students.txt"
        try:
            with open(path) as file:
                for line in file:
                    split_list = line.split("\t")
                    new_student = Student(split_list[1], split_list[0], split_list[2])
                    self.add_student(new_student.cwid, new_student)
        except FileNotFoundError:
            raise FileNotFoundError
        except ValueError:
            raise ValueError



    def readinstructor(self):
        """reads instructors data and creates instructor objects"""
        path = "/home/hannah/Documents/Schoolstuff/Books/sws810/College/instructors.txt"
        try:
            with open(path) as file:
                for line in file:
                    split_list = line.split("\t")
                    instructor = Instructor(split_list[0], split_list[1], split_list[2])
                    self.add_Instructor(instructor.cwid, instructor)
            file.close()
        except FileNotFoundError:
            raise FileNotFoundError
        except ValueError:
            raise ValueError

    def readgrades(self):
        """reads grades data and allocates it to the proper objects"""
        path = "/home/hannah/Documents/Schoolstuff/Books/sws810/College/grades.txt"
        try:
            with open(path) as file:
                for line in file:
                    split_list = line.split("\t")
                    self.get_student(split_list[0]).add_grades(split_list[2], split_list[1])
                    self.get_instructo(split_list[3].strip()).add_courses(split_list[0], split_list[1])
            file.close()
        except FileNotFoundError:
            raise FileNotFoundError
        except ValueError:
            raise ValueError

    def gettable(self):
        self.student_table = PrettyTable(['CWID', 'Name', 'Major', 'Course(s)'])
        for student in self.dict_student.values():
            self.student_table.add_row([student.cwid, student.name, student.major, list(student.courses.keys())])
        print(self.student_table)

        self.instructor_table = PrettyTable(['CWID', 'Name', 'Department', 'Student(s)'])
        for instructor in self.dict_instructor.values():
            self.instructor_table.add_row([instructor.cwid, instructor.name, instructor.department, len(instructor.courses)])
        print(self.instructor_table)


def main():
    new_repo = Repo()
    new_repo.gettable()


if __name__ == "__main__":
    main()