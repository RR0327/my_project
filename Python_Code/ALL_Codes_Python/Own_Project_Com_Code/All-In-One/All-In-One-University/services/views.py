from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from collections import OrderedDict
from datetime import date
from . models import CafeteriaMenu
from .forms import MealBookingForm
from django.contrib import messages


from .models import (
    CafeteriaMenu, 
    BusRoute, 
    BusSchedule,
    Faculty, 
    Course, 
    ClassSchedule, 
    Club, 
    Event,
    CampusBuilding
)

def index(request):
    return render(request, 'index.html')

# ---------------------
# Authentication Views
# ---------------------
def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # If "next" param was provided, go there. Otherwise, go to home.
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Example protected view
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


# ---------------------
# 1) Cafeteria Menus
# ---------------------
def cafeteria_weekly_view(request):
    """
    Renders a multi-day overview of cafeteria items, grouped by the 'day' field.
    """
    # 1) Get all menu items from the database, sorted by day (ascending)
    menu_items = CafeteriaMenu.objects.all().order_by('day')

    # 2) Create a dictionary like { day1: [item1, item2...], day2: [...], ... }
    day_groups = OrderedDict()
    for item in menu_items:
        if item.day not in day_groups:
            day_groups[item.day] = []
        day_groups[item.day].append(item)

    # 3) Pass day_groups to the template
    context = {'day_groups': day_groups}
    return render(request, 'cafeteria_multi_day.html', context)

@login_required
def create_meal_booking(request):
    if request.method == 'POST':
        form = MealBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Associate with the logged-in user
            booking.save()
            # Optionally redirect to a success page or the user's bookings
            return redirect('booking_success')
    else:
        form = MealBookingForm()

    return render(request, 'meal_booking.html', {'form': form})

# ---------------------
# 2) Bus Routes & Schedules
# ---------------------
def bus_schedules_view(request):
    routes = BusRoute.objects.all()
    schedules = BusSchedule.objects.all()
    context = {
        'routes': routes,
        'schedules': schedules
    }
    return render(request, 'bus_schedules.html', context)

# ---------------------
# 3) Class Schedules & Faculty Contacts
# ---------------------
@login_required
def class_schedules_view(request):
    # If you want to fetch class schedules for the currently logged in user, 
    # you'd create a relationship with User. For simplicity, show all:
    schedules = ClassSchedule.objects.all()
    faculty = Faculty.objects.all()
    courses = Course.objects.all()
    context = {
        'schedules': schedules,
        'faculty': faculty,
        'courses': courses
    }
    return render(request, 'class_schedules.html', context)

# ---------------------
# 4) Events & Clubs
# ---------------------
def events_view(request):
    clubs = Club.objects.all()
    events = Event.objects.all().order_by('event_date')
    context = {
        'clubs': clubs,
        'events': events
    }
    return render(request, 'events.html', context)

# ---------------------
# 5) (Optional) Campus Navigation 
# ---------------------
def campus_map_view(request):
    buildings = CampusBuilding.objects.all()
    context = {
        'buildings': buildings
    }
    return render(request, 'campus_map.html', context)

# Example JSON endpoint if you need data for an AR or interactive map
def buildings_json(request):
    buildings_data = list(CampusBuilding.objects.all().values())
    return JsonResponse(buildings_data, safe=False)
