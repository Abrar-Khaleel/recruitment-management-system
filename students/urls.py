from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Students
    path('students/', views.students_list, name='students_list'), # Note: In dashboard.html we used 'students_list'
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', views.update_student, name='update_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('export/', views.export_students_csv, name='export_csv'),
    
    # Courses (THIS WAS MISSING OR MISNAMED)
    path('courses/', views.courses_list, name='courses'),  # <--- This 'name' must match {% url 'courses' %}
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.update_course, name='update_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
]