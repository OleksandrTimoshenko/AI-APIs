import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def remove_null_fields(data):
    """Recursively removes fields with null values from a JSON-like dictionary."""

    if isinstance(data, dict):
        return {k: remove_null_fields(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [remove_null_fields(item) for item in data if item is not None]
    else:
        return data

def get_jira_ticket(ISSUE_ID, folder):
    ISSUE_URL = os.getenv("JIRA_URL") + f"/rest/api/2/issue/{ISSUE_ID}"

    # Request headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("BEARER_TOKEN")
    }
    # Make the API request
    response = requests.get(ISSUE_URL, headers=headers)

    filename = "jira_" + ISSUE_ID + '.json'
    # Check for a successful response
    if response.status_code == 200:
        issue = response.json()
        cleaned_data = remove_null_fields(issue)
        with open(filename, 'w') as json_file:
            json.dump(cleaned_data, json_file, indent=4)
        os.system(f"mv jira_{ISSUE_ID}.json {folder}")

    else:
        print(f"Failed to fetch {filename}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    get_jira_ticket("ZERAPP-1374", "./trainingData/jira")


'''

with open(ISSUE_ID + '.json', 'r') as json_file:
    issue = json.load(json_file)

# Extract important fields
issue_key = issue['key']
summary = issue['fields']['summary']
description = issue['fields']['description']
issue_type = issue['fields']['issuetype']['name']
priority = issue['fields']['priority']['name']
status = issue['fields']['status']['name']
assignee = issue['fields']['assignee']['displayName']
reporter = issue['fields']['reporter']['displayName']
created = issue['fields']['created']
updated = issue['fields']['updated']
resolution = issue['fields']['resolution']
labels = issue['fields']['labels']
timetracking = issue['fields']['timetracking']
issuelinks = issue['fields']['issuelinks']

# Print extracted fields
print(f"Issue Key: {issue_key}")
print(f"Summary: {summary}")
print(f"Description: {description}")
print(f"Issue Type: {issue_type}")
print(f"Priority: {priority}")
print(f"Status: {status}")
print(f"Assignee: {assignee}")
print(f"Reporter: {reporter}")
print(f"Created: {created}")
print(f"Updated: {updated}")
print(f"Resolution: {resolution}")
print(f"Labels: {labels}")
print(f"Timetracking: {timetracking}")
print(f"Issue Links: {issuelinks}")
'''