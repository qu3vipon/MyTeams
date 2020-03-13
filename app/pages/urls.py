from django.urls import path

from pages import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('calendar/', views.CalendarTemplateView.as_view(), name='calendar'),
    path('email/', views.EmailFormView.as_view(), name='email'),
]
