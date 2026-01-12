from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Course
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# You can keep your existing imports (Student, Course) here as well

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # We treat 'email' as the 'username' for authentication
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'index.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation 1: Passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        # Validation 2: Email already taken
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create the user (Saving email as username to match your login logic)
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            user.save()
            
            messages.success(request, "Account created! You can now login.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('register')

    return render(request, 'register.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if user exists
        if User.objects.filter(email=email).exists():
            # In a real app, you would send an email here.
            # For now, we show a success message to simulate the flow.
            messages.success(request, "If an account exists, a reset link has been sent to your email.")
            return redirect('login')
        else:
            messages.error(request, "No account found with this email address.")
            return redirect('forgot_password')

    return render(request, 'forgot-password.html')

def logout_view(request):
    logout(request)
    return redirect('login')
# ... Keep your existing dashboard, students_list, and other functions below ...


# --- DASHBOARD ---
def dashboard_view(request):
    # 1. Get real counts from the database
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    
    # 2. Get the 5 most recent students (Newest first)
    recent_students = Student.objects.order_by('-admission_date')[:5]
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'recent_students': recent_students,
    }
    return render(request, 'dashboard.html', context)

# --- STUDENT MANAGEMENT ---
def students_list(request):
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        # 1. Get data from the form
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        course_id = request.POST.get('course')
        
        # 2. Get the specific course object from the database
        course_obj = Course.objects.get(id=course_id)
        
        # 3. Create the new Student record
        Student.objects.create(
            full_name=full_name,
            email=email,
            age=age,
            course=course_obj
        )
        
        # 4. Success! Go back to the list
        return redirect('students_list')

    # GET request: Show the form with the list of courses
    courses = Course.objects.all()
    return render(request, 'add-student.html', {'courses': courses})

def update_student(request, student_id):
    # 1. Fetch the specific student to edit
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        # 3. Update the student's data with form inputs
        student.full_name = request.POST.get('full_name')
        student.email = request.POST.get('email')
        student.age = request.POST.get('age')
        
        # Get the new course ID and update the relationship
        course_id = request.POST.get('course')
        student.course = Course.objects.get(id=course_id)
        
        # 4. Save changes to database
        student.save()
        
        # 5. Redirect back to list
        return redirect('students_list')

    # 2. GET Request: Load all courses for the dropdown
    courses = Course.objects.all()
    context = {
        'student': student,
        'courses': courses
    }
    return render(request, 'edit-student.html', context)


def delete_student(request, student_id):
    # 1. Get the student or show 404 error if not found
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        # 2. If user clicked "Confirm Delete", actually delete the record
        student.delete()
        # 3. Redirect back to the main list
        return redirect('students_list')
    
    # GET request: Show the confirmation page with the student's data
    return render(request, 'delete-student.html', {'student': student})

# --- COURSE MANAGEMENT ---

def add_course(request):
    if request.method == 'POST':
        # 1. Get data from the HTML form
        name = request.POST.get('name')
        code = request.POST.get('code')
        credits = request.POST.get('credits')
        department = request.POST.get('department')
        
        # 2. Create the new Course record
        Course.objects.create(
            name=name,
            code=code,
            credits=credits,
            department=department
        )
        
        # 3. Redirect back to the course directory
        return redirect('courses')

    # GET request: Just show the form
    return render(request, 'add-course.html')

def update_course(request, course_id):
    # 1. Fetch the course object
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # 2. Update fields from the form
        course.name = request.POST.get('name')
        course.code = request.POST.get('code')
        course.credits = request.POST.get('credits')
        course.department = request.POST.get('department')
        
        # 3. Save to database
        course.save()
        
        # 4. Redirect back to directory
        return redirect('courses')

    # GET request: Pass the course object to the template
    return render(request, 'edit-course.html', {'course': course})

def delete_course(request, course_id):
    # 1. Fetch the course or return 404
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # 2. If "Confirm" is clicked, delete and redirect
        course.delete()
        return redirect('courses')
    
    # GET request: Show the confirmation page with course details
    return render(request, 'delete-course.html', {'course': course})


def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="candidates_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Full Name', 'Email', 'Course', 'Age']) # Header

    students = Student.objects.all()
    for student in students:
        writer.writerow([student.id, student.full_name, student.email, student.course.name, student.age])

    return response

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def settings_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Profile details updated successfully!')
        return redirect('settings')
    
    return render(request, 'settings.html', {'user': request.user})

def dashboard(request):
    # 1. Fetch your actual database counts
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    
    # 2. Fetch recent candidates for the table
    recent_students = Student.objects.all().order_by('-id')[:5]
    
    # 3. DEFINE THE NOTICES HERE (This is the missing part)
    notices = [
        {
            'title': 'Interview Schedule Released',
            'tag': 'NEW',
            'tag_color': 'primary', # correlates to Bootstrap class 'text-primary'
            'time': '2 hours ago'
        },
        {
            'title': 'Hiring Freeze (Q3)',
            'tag': 'URGENT',
            'tag_color': 'danger',  # correlates to Bootstrap class 'text-danger'
            'time': '1 day ago'
        },
        {
            'title': 'System Maintenance',
            'tag': 'INFO',
            'tag_color': 'info',
            'time': '3 days ago'
        }
    ]

    # 4. Pass 'notices' to the template context
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'recent_students': recent_students,
        'notices': notices,  # <--- Crucial Step
    }
    
    return render(request, 'dashboard.html', context)

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'recent_students': recent_students,
        'notices': notices, # Pass notices to template
    }
    return render(request, 'dashboard.html', context)

def students_list(request):
    # 1. Get the search query from the URL (e.g., ?search=John)
    query = request.GET.get('search')
    
    if query:
        # 2. Filter by Name, Email, or Course Name
        students = Student.objects.filter(
            Q(full_name__icontains=query) | 
            Q(email__icontains=query) |
            Q(course__name__icontains=query)
        )
    else:
        # 3. If no search, show all
        students = Student.objects.all()

    return render(request, 'students.html', {'students': students})

def courses(request):
    # 1. Grab the search text from the URL (sent by your HTML form)
    search_query = request.GET.get('search')
    
    if search_query:
        # 2. If text exists, FILTER the list
        # We search in Job Name (e.g. "Developer") OR Job ID (e.g. "JOB-01")
        courses = Course.objects.filter(
            Q(name__icontains=search_query) | 
            Q(code__icontains=search_query)
        )
    else:
        # 3. If no text, show EVERYTHING
        courses = Course.objects.all()

    # 4. Send the filtered list to the HTML
    return render(request, 'courses.html', {'courses': courses})