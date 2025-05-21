"""Configuration constants loaded from environment variables."""

import os
from dotenv import load_dotenv
load_dotenv()

# Constants
bidder_names = os.getenv("BIDDER_NAMES", "").split(",")
BIDDER_FIELD_BITRIX_ID = os.getenv("BIDDER_NAME")
BDE_FIELD_BITRIX_ID = os.getenv("BDE")
BID_REPORT_CSV_COLUMNS = os.getenv("BID_REPORT_CSV_COLUMNS", "").split(",")
DEAL_CREATION_CSV_COLUMNS = os.getenv("DEAL_CREATION_CSV_COLUMNS", "").split(",")
DEAL_LIST_ENDPOINT = os.getenv("DEAL_LIST_ENDPOINT")
DEAL_GET_ENDPOINT = os.getenv("DEAL_GET_ENDPOINT")
CATEGORY_ID = os.getenv("CATEGORY_ID")
MAX_DEALS = int(os.getenv("MAX_DEALS", "100"))
TOTAL_CLIENT_SPENDING=os.getenv("TOTAL_CLIENT_SPENDING").upper()
CLIENT_AVERAGE_HOURLY_RATE=os.getenv("CLIENT_AVERAGE_HOURLY_RATE").upper()
BIDDER_JOB_COUNTRY=os.getenv("BIDDER_JOB_COUNTRY").upper()

NUMBER_OF_BID_CONNECTS = os.getenv("NUMBER_OF_BID_CONNECTS").upper()
BIDDING_END_TIME = os.getenv("BIDDING_END_TIME").upper()
BIDDING_START_TIME = os.getenv("BIDDING_START_TIME").upper()
COVER_LETTER = os.getenv("COVER_LETTER").upper()
TOTAL_CLIENT_SPENDING=os.getenv("TOTAL_CLIENT_SPENDING").upper()
CLIENT_AVERAGE_HOURLY_RATE=os.getenv("CLIENT_AVERAGE_HOURLY_RATE").upper()
BIDDER_JOB_COUNTRY=os.getenv("BIDDER_JOB_COUNTRY").upper()
BIDDER_NAME_ID=os.getenv("BIDDER_NAME_ID").upper()

# Email config
EMAIL_FROM = os.getenv("EMAIL_FROM")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "0"))
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")

# Sample stage mapping
stage_name_mapping = {
    "C5:NEW": "New Lead",
    "C5:PREPARATION": "Acknowledge",
    "C7:PREPARATION": "Bidding Closed",
    "C5:WON": "Dont Use !!"
}

# ID → Email map
# ID_EMAIL_MAP = {
#     1: "rohitash@exoticaitsolutions.com",        # Rohitash (Admin)
#     9: "vats.gaurav52@gmail.com",                # Gaurav Vats (Admin)
#     21: "bdm.exotica@gmail.com",                 # BDM Team (Supervisor)
#     25: "tushar@exoticaitsolutions.com",         # Tushar
#     27: "karanbir.bde@exoticaitsolutions.com",   # Karanbir 
#     29: "aman@exoticaitsolutions.com",           # Aman
#     77: "abhishek.bde@exoticaitsolutions.com",   # Abhishek 
# }

ID_EMAIL_MAP = {
    1: "prateek@exoticaitsolutions.com",         # Rohitash (Admin)
    9: "prateek@exoticaitsolutions.com",         # Gaurav Vats (Admin)
    21: "exoticatestingemail@gmail.com",         # BDM Team (Supervisor)
    25: "tushar@exoticaitsolutions.com",         # Tushar
    27: "karanbir.bde@exoticaitsolutions.com",   # Karanbir 
    29: "prateek@exoticaitsolutions.com",           # Aman
    77: "abhishek.bde@exoticaitsolutions.com",   # Abhishek 
}

ADMIN_EMAIL_MAP = {
    1: "webbdeveloper24@gmail.com",
    9: "vats.gaurav52@gmail.com",
    21: "rohitash@exoticaitsolutions.com",
}