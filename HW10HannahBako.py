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
        self.failed = list()
        self.passed = list()
        self.required_courses_left = self.major.required
        self.electives_left = self.major.electives

    def add_grades(self, grade, course):
        self.courses[course] = grade
        if grade in ['A', 'A-', 'A+', 'B', 'B+', 'B-', 'C']:
            self.passed.append(course)
            if course in self.required_courses_left:
                self.required_courses_left.remove(course)
            elif course in self.electives_left:
                self.electives_left.remove(course)



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

class Major:
    def __init__(self, name, required_courses, electives):
        self.name = name
        self.required = required_courses
        self.electives = electives


class Repo:
    """This class is the repository for the data it extracts the data from the files and performs the necessary operations"""
    dict_student = dict()
    dict_instructor = dict()
    Majors = dict()
    dict_majors = defaultdict(lambda : defaultdict(list))

    def __init__(self):
        self.majors()
        self.readstudent()
        self.readinstructor()
        self.readgrades()


    def majors(self):
        path = "/home/hannah/Documents/Schoolstuff/Books/sws810/College/majors.txt"
        try:
            with open(path) as file:
                for line in file:
                    split_list = line.split("\t")
                    if split_list[1] == 'R':
                        self.dict_majors[split_list[0]]["Required"].append(split_list[2].strip())
                    else:
                        self.dict_majors[split_list[0]]["Electives"].append(split_list[2].strip())
                for item in self.dict_majors.keys():
                    new_major = Major(item, self.dict_majors[item]['Required'], self.dict_majors[item]['Electives'])
                    self.add_major(item, new_major)
        except FileNotFoundError:
            raise FileNotFoundError
        except ValueError:
            raise ValueError

    def add_student(self, cwid, student):
        self.dict_student[cwid] = student

    def add_Instructor(self, cwid, instructor):
        self.dict_instructor[cwid] = instructor

    def add_major(self, name, major):
        self.Majors[name] = major

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
                    new_student = Student(split_list[1], split_list[0], self.Majors[split_list[2].strip()])
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
                    print(split_list[0])
                    self.get_student(split_list[0]).add_grades(split_list[2], split_list[1])
                    self.get_instructo(split_list[3].strip()).add_courses(split_list[0], split_list[1])

        except FileNotFoundError:
            raise FileNotFoundError
        except ValueError:
            raise ValueError






    def gettable(self):
        self.student_table = PrettyTable(['CWID', 'Name', 'Major', 'Completed Course(s)', 'Remaining Courses', 'Remaining Electives'])
        for student in self.dict_student.values():
            self.student_table.add_row([student.cwid, student.name, student.major.name, student.passed,
                                        student.required_courses_left, student.electives_left ])
        print(self.student_table)

        self.instructor_table = PrettyTable(['CWID', 'Name', 'Department', 'Student(s)'])
        for instructor in self.dict_instructor.values():
            self.instructor_table.add_row([instructor.cwid, instructor.name, instructor.department, len(instructor.courses)])
        print(self.instructor_table)

        self.major_table = PrettyTable(['Dept', 'Required', 'Electives'])
        for  major in self.Majors.values():
            self.major_table.add_row([major.name, major.required, major.electives])
        print(self.major_table)


def main():
    new_repo = Repo()
    new_repo.gettable()


if __name__ == "__main__":
    main()