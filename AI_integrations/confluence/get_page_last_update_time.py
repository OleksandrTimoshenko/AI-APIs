# https://confluence.ontrq.com/pages/viewpreviousversions.action?pageId=508920206

import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

def work_with_datetime_object_with_timezone(date_str):
    # Convert string to datetime object with timezone
    # First, strip milliseconds and timezone separately
    date_time_obj = datetime.strptime(date_str[:-6], "%Y-%m-%dT%H:%M:%S.%f")
    timezone_str = date_str[-6:]

    # Parse timezone
    if timezone_str[0] == '-':
        tz_offset = int(timezone_str[1:3]) * 60 + int(timezone_str[4:6])
        tz_offset = -tz_offset
    elif timezone_str[0] == '+':
        tz_offset = int(timezone_str[1:3]) * 60 + int(timezone_str[4:6])
    else:
        raise ValueError("Invalid timezone format")

    # Create timezone object
    timezone = pytz.FixedOffset(tz_offset)

    # Assign timezone to datetime object
    date_time_obj = date_time_obj.replace(tzinfo=timezone)
    return date_time_obj

def get_page_history(base_url, username, password, page_id):
    endpoint = f'/rest/api/content/{page_id}?expand=version'

    # Make the request
    response = requests.get(base_url + endpoint, auth=HTTPBasicAuth(username, password))

    # Check the response status
    if response.status_code == 200:
        page_data = response.json()
        last_updated_time = page_data['version']['when']
        print(f"Last updated time: {last_updated_time}")
        return work_with_datetime_object_with_timezone(last_updated_time)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Replace with your Confluence base URL, username, and password
    base_url = os.getenv("CONFLUENCE_BASE_URL")
    username = os.getenv("CONFLUENCE_USERNAME")
    password = os.getenv("CONFLUENCE_PASSWORD")
    page_id = "508920206"
    print(get_page_history(base_url, username, password, page_id))
