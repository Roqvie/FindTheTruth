from django.urls import path, include

from . import views

urlpatterns = [
    path('getPhotos/<str:type>/<int:h>x<int:w>', views.PhotoView.as_view()),
    path('isReal/<int:pk>', views.GuesserView.as_view()),
]
