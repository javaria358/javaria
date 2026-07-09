<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Profile, Student

COURSE_DATA = [
    {
        'code': 'DDM301',
        'name': 'Pattern Making & Garment Construction',
        'instructor': 'Dr. R. Meenakshi',
        'description': 'Explore garment pattern development, cutting, and construction techniques for fashion products.',
        'department': 'Dress Designing & Manufacture',
        'semester': 4,
        'credits': 3,
        'delivery': 'In-person + lab',
        'outcomes': [
            'Develop working patterns from design sketches.',
            'Execute advanced garment construction methods.',
            'Analyze fabric behavior for tailored garments.',
        ],
    },
    {
        'code': 'CIT302',
        'name': 'Database Systems',
        'instructor': 'Prof. S. Lakshmi',
        'description': 'Learn relational design, SQL querying, and data modeling for modern applications.',
        'department': 'Computer & Information Technology',
        'semester': 4,
        'credits': 3,
        'delivery': 'Lecture + lab',
        'outcomes': [
            'Design normalized database schemas.',
            'Write SQL queries for reporting and analytics.',
            'Understand transaction and concurrency control.',
        ],
    },
    {
        'code': 'DDM304',
        'name': 'Apparel CAD',
        'instructor': 'Dr. P. Divya',
        'description': 'Use CAD tools to draft patterns, create technical flats, and produce digital garment specifications.',
        'department': 'Dress Designing & Manufacture',
        'semester': 4,
        'credits': 2,
        'delivery': 'Computer lab',
        'outcomes': [
            'Work with apparel CAD software for pattern drafting.',
            'Export digital specifications for production.',
            'Integrate CAD workflows into design projects.',
        ],
    },
    {
        'code': 'CIT304',
        'name': 'Web Application Development',
        'instructor': 'Prof. N. Revathi',
        'description': 'Build responsive web interfaces and server-backed experiences using modern web technologies.',
        'department': 'Computer & Information Technology',
        'semester': 4,
        'credits': 3,
        'delivery': 'Hybrid',
        'outcomes': [
            'Develop responsive web user interfaces.',
            'Connect front-end pages to server APIs.',
            'Apply accessibility and responsive design best practices.',
        ],
    },
]


def get_course(course_code):
    for course in COURSE_DATA:
        if course['code'] == course_code:
            return course
    raise Http404('Course not found')


@require_http_methods(["GET"])
def index(request):
    return render(request, 'student_lms/index.html', {
        'courses': COURSE_DATA[:4],
        'active_page': 'home',
    })


@require_http_methods(["GET"])
def courses(request):
    return render(request, 'student_lms/courses.html', {
        'courses': COURSE_DATA,
        'active_page': 'courses',
    })


@require_http_methods(["GET"])
def course_detail(request, course_code):
    course = get_course(course_code)
    return render(request, 'student_lms/course_detail.html', {
        'course': course,
        'active_page': 'courses',
    })


@require_http_methods(["GET"])
def about(request):
    return render(request, 'student_lms/about.html', {
        'active_page': 'about',
    })


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created. Welcome!')
            # Redirect admin users to the admin portal, students to the public student portal (index3)
            if user.is_staff:
                return redirect('admin-dashboard')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'student_lms/signup.html', {
        'form': form,
        'active_page': 'login',
    })


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.user.is_authenticated:
        # Redirect already-authenticated users to the appropriate portal
        if request.user.is_staff:
            return redirect('admin-dashboard')
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin-dashboard')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
    form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

    return render(request, 'student_lms/login.html', {
        'form': form,
        'active_page': 'login',
    })


@require_http_methods(["GET"])
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


@login_required
def dashboard(request):
    role = 'Administrator' if request.user.is_staff else 'Student'
    return render(request, 'student_lms/dashboard.html', {
        'role': role,
        'active_page': None,
    })


@require_http_methods(["GET"])
def index3(request):
    return render(request, 'student_lms/index3.html')


@require_http_methods(["GET", "POST"])
@login_required
def admin_index(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    errors = []
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        registration_number = request.POST.get('registration_number', '').strip()
        department = request.POST.get('department', '').strip()
        semester = request.POST.get('semester', '').strip()
        status = request.POST.get('status', 'active').strip()

        if not full_name:
            errors.append('Student name is required.')
        if not registration_number:
            errors.append('Registration number is required.')
        if not department:
            errors.append('Department is required.')
        if not semester:
            errors.append('Semester is required.')

        if not errors:
            Student.objects.create(
                full_name=full_name,
                registration_number=registration_number,
                department=department,
                semester=semester,
                status=status,
            )
            messages.success(request, f'Student {full_name} has been added.')
            return redirect('admin-dashboard')

    students = Student.objects.order_by('department', 'registration_number')
    return render(request, 'student_lms/admin-index.html', {
        'active_page': 'admin',
        'students': students,
        'errors': errors,
    })
=======
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Profile, Student

COURSE_DATA = [
    {
        'code': 'DDM301',
        'name': 'Pattern Making & Garment Construction',
        'instructor': 'Dr. R. Meenakshi',
        'description': 'Explore garment pattern development, cutting, and construction techniques for fashion products.',
        'department': 'Dress Designing & Manufacture',
        'semester': 4,
        'credits': 3,
        'delivery': 'In-person + lab',
        'outcomes': [
            'Develop working patterns from design sketches.',
            'Execute advanced garment construction methods.',
            'Analyze fabric behavior for tailored garments.',
        ],
    },
    {
        'code': 'CIT302',
        'name': 'Database Systems',
        'instructor': 'Prof. S. Lakshmi',
        'description': 'Learn relational design, SQL querying, and data modeling for modern applications.',
        'department': 'Computer & Information Technology',
        'semester': 4,
        'credits': 3,
        'delivery': 'Lecture + lab',
        'outcomes': [
            'Design normalized database schemas.',
            'Write SQL queries for reporting and analytics.',
            'Understand transaction and concurrency control.',
        ],
    },
    {
        'code': 'DDM304',
        'name': 'Apparel CAD',
        'instructor': 'Dr. P. Divya',
        'description': 'Use CAD tools to draft patterns, create technical flats, and produce digital garment specifications.',
        'department': 'Dress Designing & Manufacture',
        'semester': 4,
        'credits': 2,
        'delivery': 'Computer lab',
        'outcomes': [
            'Work with apparel CAD software for pattern drafting.',
            'Export digital specifications for production.',
            'Integrate CAD workflows into design projects.',
        ],
    },
    {
        'code': 'CIT304',
        'name': 'Web Application Development',
        'instructor': 'Prof. N. Revathi',
        'description': 'Build responsive web interfaces and server-backed experiences using modern web technologies.',
        'department': 'Computer & Information Technology',
        'semester': 4,
        'credits': 3,
        'delivery': 'Hybrid',
        'outcomes': [
            'Develop responsive web user interfaces.',
            'Connect front-end pages to server APIs.',
            'Apply accessibility and responsive design best practices.',
        ],
    },
]


def get_course(course_code):
    for course in COURSE_DATA:
        if course['code'] == course_code:
            return course
    raise Http404('Course not found')


@require_http_methods(["GET"])
def index(request):
    return render(request, 'student_lms/index.html', {
        'courses': COURSE_DATA[:4],
        'active_page': 'home',
    })


@require_http_methods(["GET"])
def courses(request):
    return render(request, 'student_lms/courses.html', {
        'courses': COURSE_DATA,
        'active_page': 'courses',
    })


@require_http_methods(["GET"])
def course_detail(request, course_code):
    course = get_course(course_code)
    return render(request, 'student_lms/course_detail.html', {
        'course': course,
        'active_page': 'courses',
    })


@require_http_methods(["GET"])
def about(request):
    return render(request, 'student_lms/about.html', {
        'active_page': 'about',
    })


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created. Welcome!')
            # Redirect admin users to the admin portal, students to the public student portal (index3)
            if user.is_staff:
                return redirect('admin-dashboard')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'student_lms/signup.html', {
        'form': form,
        'active_page': 'login',
    })


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.user.is_authenticated:
        # Redirect already-authenticated users to the appropriate portal
        if request.user.is_staff:
            return redirect('admin-dashboard')
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin-dashboard')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
    form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

    return render(request, 'student_lms/login.html', {
        'form': form,
        'active_page': 'login',
    })


@require_http_methods(["GET"])
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


@login_required
def dashboard(request):
    role = 'Administrator' if request.user.is_staff else 'Student'
    return render(request, 'student_lms/dashboard.html', {
        'role': role,
        'active_page': None,
    })


@require_http_methods(["GET"])
def index3(request):
    return render(request, 'student_lms/index3.html')


@require_http_methods(["GET", "POST"])
@login_required
def admin_index(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    errors = []
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        registration_number = request.POST.get('registration_number', '').strip()
        department = request.POST.get('department', '').strip()
        semester = request.POST.get('semester', '').strip()
        status = request.POST.get('status', 'active').strip()

        if not full_name:
            errors.append('Student name is required.')
        if not registration_number:
            errors.append('Registration number is required.')
        if not department:
            errors.append('Department is required.')
        if not semester:
            errors.append('Semester is required.')

        if not errors:
            Student.objects.create(
                full_name=full_name,
                registration_number=registration_number,
                department=department,
                semester=semester,
                status=status,
            )
            messages.success(request, f'Student {full_name} has been added.')
            return redirect('admin-dashboard')

    students = Student.objects.order_by('department', 'registration_number')
    return render(request, 'student_lms/admin-index.html', {
        'active_page': 'admin',
        'students': students,
        'errors': errors,
    })
>>>>>>> master
