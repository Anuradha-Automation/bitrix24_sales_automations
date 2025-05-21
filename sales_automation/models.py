from django.db import models

class TeamReport(models.Model):
    executive_name = models.CharField(max_length=255)
    number_of_bids = models.IntegerField()
    total_bids = models.IntegerField()
    name = models.CharField(max_length=255)
    bidding_start_time = models.DateTimeField()
    bidding_end_time = models.DateTimeField()
    total_time_seconds = models.IntegerField()
    total_client_spending = models.DecimalField(max_digits=12, decimal_places=2)
    client_average_hour_rate = models.DecimalField(max_digits=8, decimal_places=2)
    bidder_job_country = models.CharField(max_length=255)
    pipeline = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.executive_name} - {self.name}"
