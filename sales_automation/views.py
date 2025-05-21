from django.shortcuts import render
from .create_bid_report import main  
from django.http import JsonResponse
from .models import TeamReport

def run_bid_report(request):
    try:
        print("--------------starrtt--------")
        main()  # Make sure this function exists and does not require parameters
        return JsonResponse({"status": "success", "message": "Report generated and emailed successfully."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def sent_email(request):
    reports = TeamReport.objects.all()

    print("----->>",reports)    
    return 0
