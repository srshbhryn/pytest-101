from django.urls import path

from courses import views

urlpatterns = [
    path('view_courses/', views.view_courses, name='view_courses'),
    path('add_student/', views.add_student, name='add_student'),
]