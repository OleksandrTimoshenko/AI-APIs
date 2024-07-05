import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

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

    # Check for a successful response
    if response.status_code == 200:
        issue = response.json()
        with open("jira_" + ISSUE_ID + '.json', 'w') as json_file:
            json.dump(issue, json_file, indent=4)
        os.system(f"mv jira_{ISSUE_ID}.json {folder}")

    else:
        print(f"Failed to fetch issue: {response.status_code} - {response.text}")

if __name__ == "__main__":
    get_jira_ticket("jira_ZERAPP-1374", "./trainingData/jira")


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