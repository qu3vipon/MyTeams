from django.urls import path, include

# app_name = 'members'
urlpatterns = [
    path('', include('allauth.urls'))
]
