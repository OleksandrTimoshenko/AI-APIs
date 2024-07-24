import requests
import os
import re
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from download_conf_page import get_page
from get_page_last_update_time import get_page_history

load_dotenv()

def get_pages_in_space(space):
    # Define the endpoint you want to access, for example, getting the current user
    #endpoint = '/rest/api/content'
    #endpoint = '/rest/api/space'
    endpoint = f'/rest/api/space/{space}/content'
    print(endpoint)

    # Make the request
    response = requests.get(base_url + endpoint, auth=HTTPBasicAuth(username, password))

    page_dict = {}
    # Check the response status
    if response.status_code == 200:
        print("Request was successful")
        data = response.json()
        for item in data['page']['results']:
            if item['type'] == 'page':
                page_dict[item['title']] = item['id']
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
    return page_dict

def page_was_updated(updated_date):
    current_date = datetime.now(updated_date.tzinfo)
    difference = current_date - updated_date
    return difference <= timedelta(days=int(os.getenv("CONFLUENCE_UPDATING_PERIOD_IN_DAYS")))

if __name__ == "__main__":
    # Replace with your Confluence base URL, username, and password
    base_url = os.getenv("CONFLUENCE_BASE_URL")
    username = os.getenv("CONFLUENCE_USERNAME")
    password = os.getenv("CONFLUENCE_PASSWORD")
    confluence_pages_dict = get_pages_in_space(os.getenv("CONFLUENCE_PROJECT_KEY"))
    folder = "./trainingData/confluence/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    for page_title, page_id in confluence_pages_dict.items():
        if page_was_updated(get_page_history(base_url, username, password, page_id)):
            page_title = re.sub(r'[^\w]', '_', page_title)
            get_page(base_url, username, password, page_id, page_title, folder)