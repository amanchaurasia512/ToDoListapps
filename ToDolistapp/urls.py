from django.contrib import admin
from django.urls import path
from .views import TaskList ,Registerpage ,customlogin ,TaskCreateView ,TaskUpdateView,TaskDeleteView
from django.contrib.auth.views import LogoutView 
from .import views
urlpatterns = [
    path('', TaskList.as_view(),name='task'),
    path('register/', Registerpage.as_view(), name='register'),
    path('customlogin',customlogin.as_view(), name='customlogin'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('logout/',LogoutView.as_view(next_page='customlogin'), name='logout'),
    path('Task-CreateView/',TaskCreateView.as_view(),name='Task-CreateView'),
    path('Task-update/<int:pk>/', TaskUpdateView.as_view(),name='Task-update'),
    path('Task-delete/<int:pk>/', TaskDeleteView.as_view() , name='Task-delete')
    
]
