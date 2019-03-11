# coding = UTF-8

import random
import copy

from class_DAMatch import Male, Female, StableMatcher

class simulation_matcher:
    def __init__(self, student_numbers, teacher_numbers,
                 teacher_max_accepted=1):
        self._student_numbers = student_numbers
        self._teacher_numbers = teacher_numbers
        self._teacher_max_accepted = teacher_max_accepted
        self._students_preferences = self.__students_preferences()
        self._teachers_preferences = self.__teachers_preferences()

    def match(self):
        students = []
        for student in self._students_preferences:
            students.append(Male(student[0], student[1]))
        teachers = []
        for teacher in self._teachers_preferences:
            teachers.append(Female(teacher[0], teacher[1], teacher[2]))

        matcher = StableMatcher(men=students, women=teachers)
        matcher.match(echo=False)
        return matcher.result

    def __students_preferences(self):
        number = int(self._student_numbers)
        teachers_number = int(self._teacher_numbers)
        generated_teachers = [''.join(['Teacher', str(n)])
                              for n in range(1, teachers_number+1)]
        students = []
        for i in range(1, number+1):
            copy_generated_teachers = copy.copy(generated_teachers)
            random.shuffle(copy_generated_teachers)
            students.append((''.join(['Student', str(i)]),
                             copy_generated_teachers))

        return students

    def __teachers_preferences(self):
        number = int(self._teacher_numbers)
        students_number = int(self._student_numbers)
        max_accepted = int(self._teacher_max_accepted)
        generated_students = [''.join(['Student', str(n)])
                              for n in range(1, students_number+1)]
        teachers = []
        for i in range(1, number+1):
            copy_generated_students = copy.copy(generated_students)
            random.shuffle(copy_generated_students)
            teachers.append((''.join(['Teacher', str(i)]),
                             copy_generated_students, max_accepted))

        return teachers

    @property
    def students_preferences(self):
        return self._students_preferences

    @property
    def teachers_preferences(self):
        return self._teachers_preferences

if __name__ == '__main__':
    matcher = simulation_matcher(student_numbers=2, teacher_numbers=2)
    print(matcher.teachers_preferences)
    print(matcher.students_preferences)
    print(matcher.match())
