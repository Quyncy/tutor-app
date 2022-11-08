from django.urls import path

from userAPI import views

app_name = 'userAPI'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create')

]