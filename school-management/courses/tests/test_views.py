
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.urls import reverse

from pytest_django import asserts

from accounts.models import User
from courses.models import Course

class ViewGradesTest(TestCase):
    fixtures = ['data']

    def setUp(self):
        first_teacher = User.teachers.order_by('id').first()
        second_teacher = User.teachers.order_by('id').last()
        first_student = User.students.order_by('id').first()
        second_student = User.students.order_by('id').last()
        first_course = Course.objects.create(teacher=first_teacher)
        first_course.students.add(first_student)
        second_course = Course.objects.create(teacher=second_teacher)
        second_course.students.add(second_student)
        self.client = Client()
        self.url = reverse('view_courses')

    def test_view_courses_for_anonymous_user(self):
        client = Client()
        response = client.get(self.url)
        response.status_code == 403

    def test_view_courses_for_teacher(self):
        teacher = User.teachers.first()
        excepted_courses = Course.objects.filter(teacher=teacher)
        client = Client()
        client.force_login(teacher)
        response = client.get(self.url)
        asserts.assertTemplateUsed(response, 'courses/view_teacher_courses.html')
        asserts.assertQuerysetEqual(list(response.context['courses']), excepted_courses)

    def test_view_courses_for_student(self):
        student = User.students.first()
        excepted_courses = Course.objects.filter(students=student)
        client = Client()
        client.force_login(student)
        response = client.get(self.url)
        asserts.assertTemplateUsed(response, 'courses/view_student_courses.html')
        asserts.assertQuerysetEqual(list(response.context['courses']), excepted_courses)


class ViewGradesTest(TestCase):
    fixtures = ['data']

    def setUp(self):
        first_teacher = User.teachers.order_by('id').first()
        second_teacher = User.teachers.order_by('id').last()
        first_student = User.students.order_by('id').first()
        second_student = User.students.order_by('id').last()
        first_course = Course.objects.create(teacher=first_teacher)
        first_course.students.add(first_student)
        second_course = Course.objects.create(teacher=second_teacher)
        second_course.students.add(second_student)
        self.client = Client()
        self.url = reverse('view_courses')

    def test_view_courses_for_anonymous_user(self):
        client = Client()
        response = client.get(self.url)
        response.status_code == 403

    def test_view_courses_for_teacher(self):
        teacher = User.teachers.first()
        excepted_courses = Course.objects.filter(teacher=teacher)
        client = Client()
        client.force_login(teacher)
        response = client.get(self.url)
        asserts.assertTemplateUsed(response, 'courses/view_teacher_courses.html')
        asserts.assertQuerysetEqual(list(response.context['courses']), excepted_courses)

    def test_view_courses_for_student(self):
        student = User.students.first()
        excepted_courses = Course.objects.filter(students=student)
        client = Client()
        client.force_login(student)
        response = client.get(self.url)
        asserts.assertTemplateUsed(response, 'courses/view_student_courses.html')
        asserts.assertQuerysetEqual(list(response.context['courses']), excepted_courses)


@override_settings(COULD_TEACHERS_ADD_STUDENTS_TO_COURSES=True)
class AddStudentTest(TestCase):
    fixtures = ['data']

    def setUp(self):
        self.teacher = User.teachers.first()
        self.student = User.students.get(pk=3)
        self.other_teacher = User.teachers.last()
        Course.objects.create(teacher=self.teacher)
        self.url = reverse('add_student')

    @override_settings(COULD_TEACHERS_ADD_STUDENTS_TO_COURSES=False)
    def test__disabled_settings_(self):
        self.client.force_login(self.teacher)
        response = self.client.get(self.url)
        assert response.status_code == 403

    def test_view_courses_for_anonymous_user(self):
        client = Client()
        response = client.get(self.url)
        response.status_code == 403

    def test_student_attempt(self):
        client = Client()
        client.force_login(self.student)
        response = client.get(self.url)
        assert response.status_code == 403

    def test_invalid_post_data(self):
        client = Client()
        client.force_login(self.other_teacher)
        course_id = Course.objects.first().id
        student_id = self.student.id
        response = client.post(self.url, {
            'course_id': course_id,
            'student_id': student_id,
        })
        assert response.status_code == 404
        client.force_login(self.teacher)
        response = client.post(self.url, {
            'course_id': course_id,
            'student_id': 1000,
        })
        assert response.status_code == 404

    def test_valid_post_data(self):
        client = Client()
        client.force_login(self.teacher)
        course_id = Course.objects.first().id
        student_id = 4
        response = client.post(self.url, {
            'course_id': course_id,
            'student_id': student_id,
        })
        assert response.status_code == 200
        asserts.assertTemplateUsed('courses/add_student_to_course.html')

