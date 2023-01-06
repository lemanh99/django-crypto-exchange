from django.urls import path

from crypto.user import views

urlpatterns = [
    path('telegram/tracker/create', views.create_action_tracking_telegram, name='create_action_tracking_telegram'),
    path('telegram/<str:uuid>/tracker', views.get_user_telegram_tracker_by_uuid,
         name='get_user_telegram_tracker_by_uuid'),
    path('telegram/tracker/<str:uuid>/delete', views.delete_user_telegram_tracker_by_uuid,
         name='delete_user_telegram_tracker_by_uuid'),
    path('telegram/tracker/clear-data', views.clear_data_user_telegram_tracker,
         name='clear_data_user_telegram_tracker'),
]
