from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_candidate/<int:election_id>/', views.add_candidate_to_election, name='add_candidate'),
    path(r'issue_vote/<int:election_id>/<str:randomstr>', views.issue_vote, name='issue_vote'),
    path('add_candidate', views.create_candidate, name='add_candidate'),
    path('add_election', views.add_election, name='add_election'),
    path('create_url/<int:election_id>/', views.create_election_url, name='create_url'),
    path('get_result/<int:election_id>/', views.get_result, name='get_result'),
    path('login', views.user_login, name='user_login'),
    path('register', views.user_register, name='user_register'),
    path('logout', views.user_logout, name='logout'),
    path('verify', views.verify, name='verify'),
    path('profile/<int:candidate_id>/', views.candidate_profile, name='candidate_profile'),
    path('pubprofile/', views.personal_profile, name='public_profile')
]
