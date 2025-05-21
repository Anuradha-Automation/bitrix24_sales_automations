"""Generates and stores weekly bid reports from Bitrix24 API."""

import os
import sys
import json
import time
import decimal
import requests

from decimal import Decimal
from datetime import datetime, timedelta

from .models import TeamReport  # Adjust import as per your Django app name
from .logs_setup_file import setup_logging
from sales_automation.config import (
    DEAL_LIST_ENDPOINT, DEAL_GET_ENDPOINT,
    CATEGORY_ID, MAX_DEALS, NUMBER_OF_BID_CONNECTS,
    BIDDING_END_TIME, BIDDING_START_TIME,
    TOTAL_CLIENT_SPENDING, CLIENT_AVERAGE_HOURLY_RATE,
    BIDDER_JOB_COUNTRY, BIDDER_NAME_ID
)

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup logger
MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logging(MODULE_NAME)

# Load country map
country_map = {}
try:
    with open(os.path.abspath("sales_automation/country_map.json"), 'r', encoding='utf-8') as file:
        raw_map = json.load(file)
        country_map = {
            item["ID"]: item["VALUE"]
            for item in raw_map["result"]["22"]["LIST"]
        }
except Exception as e:
    logger.error("❌ Failed to load country map: %s", str(e))


def safe_decimal(value):
    """Safely convert a value to Decimal."""
    try:
        return Decimal(str(value))
    except (ValueError, TypeError, decimal.InvalidOperation):
        return Decimal('0')


def fetch_deals():
    """Fetches and returns matched deal data from Bitrix24."""
    start = 0
    total_fetched = 0
    deal_blocks = []
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    filter_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')

    while True:
        payload = {
            "SELECT": ["ID"],
            "FILTER": {
                "CATEGORY_ID": CATEGORY_ID,
                ">=DATE_CREATE": filter_date
            },
            "ORDER": {"TITLE": "ASC"},
            "start": start
        }

        try:
            response = requests.post(DEAL_LIST_ENDPOINT, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("❌ Error fetching deal list: %s", str(e))
            sys.exit(1)

        result = response.json()
        deals = result.get("result", [])
        if not deals:
            break

        logger.info("📦 Processing %s deals (start=%s)", len(deals), start)

        for deal in deals:
            if total_fetched >= MAX_DEALS:
                break

            deal_id = deal["ID"]
            try:
                detail_resp = requests.post(DEAL_GET_ENDPOINT, headers=headers, json={"id": deal_id}, timeout=30)
                detail_resp.raise_for_status()
                deal_data = detail_resp.json().get("result", {})
                deal_blocks.append(deal_data)
                total_fetched += 1
            except requests.RequestException:
                logger.warning("⚠️ Failed to fetch details for deal ID: %s", deal_id)

        if "next" in result:
            start = result["next"]
            time.sleep(0.2)
        else:
            break

    return deal_blocks


def process_deal_data(deal_blocks):
    """Processes and saves deal data into the TeamReport model."""
    if not deal_blocks:
        logger.info("⚠️ No matching deals found.")
        return

    logger.info("✅ Total matched deals: %s", len(deal_blocks))

    for deal in deal_blocks:
        try:
            start_time = deal.get(BIDDING_START_TIME)
            end_time = deal.get(BIDDING_END_TIME)
            total_time_seconds = 0

            if start_time and end_time:
                total_time_seconds = int(
                    (datetime.fromisoformat(end_time) - datetime.fromisoformat(start_time)).total_seconds()
                )

            country_ids = deal.get(BIDDER_JOB_COUNTRY, [])
            if isinstance(country_ids, str):
                country_ids = [country_ids]
            elif not isinstance(country_ids, list):
                country_ids = []

            country_names = [country_map.get(str(cid), 'Not Selected') for cid in country_ids]
            country_string = ", ".join(country_names)

            connects = int(deal.get(NUMBER_OF_BID_CONNECTS, 0) or 0)

            report = TeamReport.objects.create(
                executive_name=deal.get(BIDDER_NAME_ID),
                number_of_bids=1,
                total_bids=connects,
                name=deal.get("TITLE", ""),
                bidding_start_time=start_time,
                bidding_end_time=end_time,
                total_time_seconds=total_time_seconds,
                total_client_spending=safe_decimal(deal.get(TOTAL_CLIENT_SPENDING)),
                client_average_hour_rate=safe_decimal(deal.get(CLIENT_AVERAGE_HOURLY_RATE)),
                bidder_job_country=country_string,
                pipeline="Sales_Management"
            )

            logger.info("✅ Saved report for: %s", report.executive_name)

        except Exception as e:
            logger.error("❌ Failed to process deal ID %s: %s", deal.get("ID"), str(e))


def main():
    """Main function to generate and save the bid report."""
    logger.info("🚀 Starting bid report generation...")
    deal_blocks = fetch_deals()
    process_deal_data(deal_blocks)
    logger.info("🏁 Bid report generation completed.")


if __name__ == "__main__":
    main()
