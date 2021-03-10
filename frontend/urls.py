from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page),
    path('person', views.person),
    path('cat', views.cat),
    path('about', views.about)
]