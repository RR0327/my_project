from django.urls import path
from . import views
from .views import create_meal_booking
from django.views.generic import TemplateView
from django.urls import path, include
from .views import user_login_view, user_login

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    # path('admin/', admin.site.urls),
    path('login/', user_login_view, name='login'),  
    path('accounts/', include('django.contrib.auth.urls')),  
    path('cafeteria/', views.cafeteria_weekly_view, name='cafeteria_main'),
    path('cafeteria/multi-day/', views.cafeteria_weekly_view, name='cafeteria_multi_day'),
    path('meal-booking/', views.create_meal_booking, name='meal_booking'),
    path('booking-success/', TemplateView.as_view(template_name='booking_success.html'), name='booking_success'),
    path('bus-schedules/', views.bus_schedules_view, name='bus_schedules'),
    path('schedule/', views.class_schedule_view, name='class_schedule'),
    path('schedule/add/', views.add_class_schedule, name='add_schedule'),
    path('events/', views.events_view, name='events'),
    path('campus-map/', views.campus_map_view, name='campus_map'),
    path('buildings-json/', views.buildings_json, name='buildings_json'),  # Optional JSON endpoint
]
