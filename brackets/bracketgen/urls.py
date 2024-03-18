from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('tournament/<str:id>', views.tournament, name="tournament"),
	path('accounts/', include('django.contrib.auth.urls')),
	path('mytournaments/', views.myTournaments.as_view(), name="my-tournaments"),
	path('myinfo/', views.userInfo.as_view(), name="my-info"),
	path('updateprofile', views.updateUserInfo, name="update-info"),
	path('signup/',views.SignUp.as_view(), name='signup'),
]

"""
All Mappings produced from accounts/

accounts/ login/ [name='login']
accounts/ logout/ [name='logout']
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']
"""

