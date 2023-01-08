from django.urls import path

from crypto.user import views

urlpatterns = [
    path('telegram/tracker/create', views.create_action_tracking_telegram, name='create_action_tracking_telegram'),
    path('telegram/<str:user_id>/tracker', views.get_user_telegram_tracker_by_user_id,
         name='get_user_telegram_tracker_by_user_id'),
    path('telegram/<str:user_id>/update', views.update_user_telegram_tracker_by_user_id,
         name='update_user_telegram_tracker_by_user_id'),
    path('telegram/tracker/<str:user_id>/delete', views.delete_user_telegram_tracker_by_user_id,
         name='delete_user_telegram_tracker_by_user_id'),
    path('telegram/tracker/clear-data', views.clear_data_user_telegram_tracker,
         name='clear_data_user_telegram_tracker'),
]
