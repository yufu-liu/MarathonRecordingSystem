from django.urls import path
from .views import new_marathon, get_marathon, delete_marathon, update_checkpoints, \
    get_racer_results, modify_gun_time, modify_station_name, modify_km_group, modify_age_gender_group,\
    update_status

urlpatterns = [
    path('new_marathon/', new_marathon, name='new_marathon'),
    path('get_marathon/', get_marathon, name='get_marathon'),
    path('delete_marathon/', delete_marathon, name='delete_marathon'),
    path('update_checkpoints/', update_checkpoints, name='update_checkpoints'),
    path('get_racer_results/', get_racer_results, name='get_racer_results'),
    path('modify_gun_time/', modify_gun_time, name='modify_gun_time'),
    path('modify_station_name/', modify_station_name, name='modify_station_name'),
    path('modify_km_group/', modify_km_group, name='modify_km_group'),
    path('modify_age_gender_group/', modify_age_gender_group, name='modify_age_gender_group'),
    path('update_status/', update_status, name='update_status'),
]

