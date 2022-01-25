from django.db import models

from accounts.models import User


class Course(models.Model):
    teacher = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='+')

    @property
    def average_grade(self):
        return self.students.aggregate(avg=models.Avg('grade')).get('avg')


class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(default=None)
