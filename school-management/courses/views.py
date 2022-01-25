from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from accounts.models import User
from courses.models import Course

@login_required
def view_courses(request):
    if request.user.is_teacher:
        courses = Course.objects.filter(teacher=request.user)
        return render(request, 'courses/view_teacher_courses.html', {
            'courses': courses,
        })
    courses = Course.objects.filter(students=request.user)
    return render(request, 'courses/view_student_courses.html', {
        'courses': courses,
    })


@login_required
def add_student(request):
    if not request.user.is_teacher or not settings.COULD_TEACHERS_ADD_STUDENTS_TO_COURSES:
        return HttpResponseForbidden()
    if request.method == 'POST':
        course_id = request.POST['course_id']
        student_id = request.POST['student_id']
        student = get_object_or_404(User.students, pk=student_id)
        course = get_object_or_404(Course.objects.filter(teacher=request.user), pk=course_id)
        course.students.add(student)
    return render(request, 'courses/add_student_to_course.html', {})
