"""
lists URL Configuration
"""
from lists.views import home_page
from django.urls import path


urlpatterns = [
    path('', home_page, name='home')
]

