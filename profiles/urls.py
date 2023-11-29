from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_profiles, name='all_profiles'),
    path('<user_id>', views.view_profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('connect/<id>', views.add_connection, name='connect'),
    path('disconnect/<id>', views.remove_connection, name='remove_connection'),
]