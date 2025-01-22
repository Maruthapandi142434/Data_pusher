from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.account_list),
    path('accounts/<int:account_id>/destinations/', views.get_destinations_for_account),
    path('destinations/', views.destination_list),
    path('server/incoming_data', views.incoming_data),
]
