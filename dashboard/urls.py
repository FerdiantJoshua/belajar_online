from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('main/', views.DashboardMainView.as_view(), name='main'),
    path('bookings/', views.DashboardBookingsListView.as_view(), name='list_bookings'),
    path('history/', views.DashboardHistoryListView.as_view(), name='list_history'),
]
