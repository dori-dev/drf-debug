from django.urls import path
from tracking import views


app_name = 'tracking'
urlpatterns = [
    path('', views.Home.as_view()),
]
