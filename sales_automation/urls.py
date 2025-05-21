
from django.urls import path
from .views import run_bid_report,sent_email

urlpatterns = [
    path('run_report/', run_bid_report, name='run_bid_report'),
    path('sent_email/', sent_email, name='sent_email'),

]
