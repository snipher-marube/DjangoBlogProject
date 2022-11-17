from django.urls import path

from . import views
app_name = 'newsletter'

urlpatterns = [
    path('newsletter/', views.newsletter_subscribe, name='subscribe'),
    path('unsubscribe/', views.newsletter_unsubscribe, name='unsubscribe'),
    path('send-newsletter/', views.send_newsletter, name='send_newsletter'),
]
