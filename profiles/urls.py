from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_profiles, name='all_profiles'),
    path('<user_id>', views.view_profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('connect/<id>', views.add_connection, name='connect'),
    path('disconnect/<id>', views.remove_connection, name='remove_connection'),
    path('add_job/', views.add_job, name='add_job'),
    path('edit_job/<id>', views.edit_job, name='edit_job'),
    path('delete_job/<id>', views.delete_job, name='delete_job'),
]