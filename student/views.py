from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Avg

from .models import (
    UserStudyProfile,
    TopicExplanation,
    InterviewQuestionSet,
    Quiz,
    ChatMessage
)


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([first_name, username, email, password]):
            messages.error(request, 'Please fill all required fields.')

        elif len(password) < 6:
            messages.error(request, 'Password must contain at least 6 characters.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already registered.')

        else:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                UserStudyProfile.objects.create(user=user)

            login(request, user)
            messages.success(request, 'Welcome to EduMind!')
            return redirect('dashboard')

    return render(request, 'register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if request.POST.get('remember_me') != 'on':
                request.session.set_expiry(0)

            UserStudyProfile.objects.get_or_create(user=user)

            messages.success(request, 'Login successful!')
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully.')

    return redirect('home')


@login_required
def dashboard(request):
    profile, created = UserStudyProfile.objects.get_or_create(
        user=request.user
    )

    quizzes = Quiz.objects.filter(
        user=request.user,
        completed=True
    )

    average_score = quizzes.aggregate(
        average=Avg('percentage')
    )['average'] or 0

    context = {
        'profile': profile,
        'total_sessions': profile.total_sessions,
        'completed_quizzes': quizzes.count(),
        'average_score': round(average_score, 1),
        'topics': TopicExplanation.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5],
        'interviews': InterviewQuestionSet.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5],
    }

    return render(request, 'dashboard.html', context)