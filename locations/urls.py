from django.urls import path

from . import views

urlpatterns= [
    path('',views.index, name='index'),
    path('allusers',views.all_users, name='all_users'),
    path('register',views.register_user, name='register_user'),
    path('<int:user_id>/',views.user, name='user'),
    path('<int:user_id>/last',views.last_location, name='last_location'),
    path('<int:user_id>/updatelocation',views.update_location, name='update_location')
]