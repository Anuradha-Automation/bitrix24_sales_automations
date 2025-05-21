from django.contrib import admin
from .models import TeamReport

@admin.register(TeamReport)
class TeamReportAdmin(admin.ModelAdmin):
    list_display = (
        'executive_name',
        'number_of_bids',
        'total_bids',
        'name',
        'bidding_start_time',
        'bidding_end_time',
        'total_time_seconds',
        'total_client_spending',
        'client_average_hour_rate',
        'bidder_job_country',
        'pipeline',
    )
    list_filter = ('pipeline', 'executive_name', 'bidder_job_country')
    search_fields = ('executive_name', 'name')
    ordering = ('-bidding_start_time',)
