import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from ticket_info import get_jira_ticket

load_dotenv()

def get_tickets_list():
    # JQL query to fetch issues assigned to the specified user in the project
    # see more about JQL - https://support.atlassian.com/jira-service-management-cloud/docs/what-is-advanced-search-in-jira-cloud/
    JQL = "project = " + os.getenv("PROJECT_KEY") + " " + os.getenv("JQL_QUERY")

    # Jira API endpoint for searching issues
    SEARCH_URL = os.getenv("JIRA_URL") + "/rest/api/2/search"

    # Request headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv('BEARER_TOKEN')
    }

    # TODO: move 'maxResults' to .env variables
    # Request parameters
    params = {
        "jql": JQL,
        "maxResults": 2000,  # Adjust the number of results as needed
        "fields": "key,status,updated"  # Specify the fields you want to retrieve
    }

    # Make the API request
    response = requests.get(SEARCH_URL, headers=headers, params=params)

    #print(response.json())

    # Check for a successful response
    if response.status_code == 200:
        tickets_dict = {}
        issues = response.json().get("issues", [])
        for issue in issues:
            tickets_dict[issue['key']] = [issue['fields']['status']['name'], issue['fields']['updated']]
    else:
        print(f"Failed to fetch issues: {response.status_code} - {response.text}")
    return tickets_dict

def ticket_was_updated(updated_date):
    current_date = datetime.now(updated_date.tzinfo)
    difference = current_date - updated_date
    return difference <= timedelta(days=int(os.getenv("UPDATING_PERIOD_IN_DAYS")))

def get_updated_tickets(jira_tickets_dict):
    updated_tickets = []
    for ticket_name, value in jira_tickets_dict.items():
        if value[0] != "Closed" and ticket_was_updated(datetime.strptime(value[1], '%Y-%m-%dT%H:%M:%S.%f%z')):
            updated_tickets.append(ticket_name)
    return updated_tickets


if __name__ == "__main__":
    folder = "./trainingData/jira/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    all_tickets = get_tickets_list()
    updated_tickets = get_updated_tickets(all_tickets)
    for ticket in updated_tickets:
        get_jira_ticket(ticket, folder)