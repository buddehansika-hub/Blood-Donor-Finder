from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),

    path('donor-profile/', views.donor_profile, name='donor_profile'),

    path('search/', views.search_donor, name='search'),

    path('request/<int:donor_id>/', views.send_request, name='send_request'),
path('my-requests/', views.my_requests, name='my_requests'),
path('received-requests/', views.received_requests, name='received_requests'),
path('update-request/<int:request_id>/<str:status>/', views.update_request, name='update_request'),
path('edit-profile/', views.edit_profile, name='edit_profile'),
]