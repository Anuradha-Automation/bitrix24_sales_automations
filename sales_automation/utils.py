"""Utility functions for email handling based on employee ID and bidder name."""

import os
import csv

from .config import   ID_EMAIL_MAP,ADMIN_EMAIL_MAP,BID_REPORT_CSV_COLUMNS


def get_employee_id(bidder_name):
    """
    Returns the employee ID based on the bidder name.
    """
    key = f"EMPLOYEE_ID_{bidder_name.upper()}"
    return os.getenv(key)


def get_all_email_to(employee_id, unique_ids):
    """
    Returns a list of email addresses:
    - The email corresponding to the given employee_id
    - Emails for all IDs in unique_ids (a tuple of sets)
    """

    emails = []

    employee_id = int(employee_id)
    if email := ID_EMAIL_MAP.get(employee_id):
        emails.append(email)

    for uid_set in unique_ids:
        for uid in uid_set:
            uid = int(uid)
            if email := ID_EMAIL_MAP.get(uid):
                emails.append(email)

    return list(set(emails))


# def get_all_email_to(employee_id, unique_ids):
#     """
#     Returns a list of email addresses:
#     - The email corresponding to the given employee_id
#     - Emails for all IDs in unique_ids (set or list of IDs)
#     """
#     emails = []

#     if email := ID_EMAIL_MAP.get(int(employee_id)):
#         emails.append(email)

#     for uid in unique_ids:
#         try:
#             uid = int(uid)
#             if email := ID_EMAIL_MAP.get(uid):
#                 emails.append(email)
#         except (ValueError, TypeError):
#             continue

#     return list(set(emails))

def get_admin_email_to(unique_ids):
    """
    Returns a list of email addresses for admins only:
    - Emails for all IDs in unique_ids that are admins.
    """
    emails = []

    for uid in unique_ids:
        try:
            uid = int(uid)
            if email := ADMIN_EMAIL_MAP.get(uid):
                emails.append(email)
        except (ValueError, TypeError):
            continue

    return list(set(emails))


def export_csv(csv_filename, data_rows,CSV_COLUMNS,logger):
    """
    Export the data rows to a CSV file.

    Args:
        csv_filename (str): The name of the file to save the CSV.
        data_rows (list): The data to be written into the CSV file.
    """
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(CSV_COLUMNS)
        writer.writerows(data_rows)
    logger.info("✅ Custom CSV exported: %s", csv_filename)


