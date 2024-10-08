import requests
import json
import os, re
from dotenv import load_dotenv

load_dotenv(os.path.dirname(os.path.abspath(__file__)) + "/../../OpenAI/.env")

def remove_null_fields(data):
    """Recursively removes fields with null values from a JSON-like dictionary."""

    if isinstance(data, dict):
        return {k: remove_null_fields(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [remove_null_fields(item) for item in data if item is not None]
    else:
        return data

def get_important_fields(issue):
    issue_data = {}

    # Extract fields with error handling
    try:
        issue_data['Project'] = issue['fields']['project']['name']
    except:
        issue_data['Project'] = None

    try:
        issue_data['Issue Key'] = issue['key']
    except KeyError:
        issue_data['Issue Key'] = None

    try:
        issue_data['Summary'] = issue['fields']['summary']
    except KeyError:
        issue_data['Summary'] = None

    try:
        issue_data['Description'] = issue['fields']['description']
    except KeyError:
        issue_data['Description'] = None

    try:
        issue_data['Issue Type'] = issue['fields']['issuetype']['name']
    except KeyError:
        issue_data['Issue Type'] = None

    try:
        issue_data['Status'] = issue['fields']['status']['name']
    except KeyError:
        issue_data['Status'] = None

    try:
        issue_data['Priority'] = issue['fields']['priority']['name']
    except KeyError:
        issue_data['Priority'] = None

    try:
        issue_data['Resolution'] = issue['fields']['resolution']
    except KeyError:
        issue_data['Resolution']  = None

    try:
        issue_data['Resolution date'] = issue['fields']['resolutiondate']
    except KeyError:
        issue_data['Resolution date'] = None

    try:
        issue_data['Assignee'] = issue['fields']['assignee']['displayName']
    except KeyError:
        issue_data['Assignee'] = None

    try:
        issue_data['Reporter'] = issue['fields']['reporter']['displayName']
    except KeyError:
        issue_data['Reporter'] = None

    try:
        issue_data['Creator'] = issue['fields']['creator']['name']
    except KeyError:
        issue_data['Creator'] = None

    try:
        issue_data['Created'] = issue['fields']['created']
    except KeyError:
        issue_data['Created'] = None

    try:
        issue_data['Updated'] = issue['fields']['created']
    except KeyError:
        issue_data['Updated'] = None

    try:
        issue_data["Last viewed"] = issue['fields']['lastViewed']
    except KeyError:
        issue_data["Last viewed"] = None

    try:
        issue_data["Votes"] = issue['fields']['votes']['votes']
    except KeyError:
        issue_data["Votes"] = None

    try:
        issue_data["Watchers"] = issue['fields']['watches']['watchCount']
    except KeyError:
        issue_data["Watchers"] = None

    try:
        issue_data["Attachments"] = issue['fields']['attachment']
    except KeyError:
        issue_data["Attachments"] = None

    try:
        issue_data['Timetracking'] = issue['fields']['timetracking']
    except KeyError:
        issue_data['Timetracking'] = None

    try:
        issue_data["Timeestimate"] = issue['fields']['timeestimate']
    except KeyError:
        issue_data["Timeestimate"] = None

    try:
        issue_data["Timespent"] = issue['fields']['timespent']
    except KeyError:
        issue_data["Timespent"] = None

    try:
        issue_data['Labels'] = issue['fields']['labels']
    except KeyError:
        issue_data['Labels'] = None

    try:
        issue_data['Issue Links'] = issue['fields']['issuelinks']
    except KeyError:
        issue_data['Issue Links'] = None

    try:
        issue_data['Fix versions'] = issue['fields']['fixVersions']
    except KeyError:
        issue_data['Fix versions'] = None

    # Extract comments with author name and body
    try:
        comments = issue['fields']['comment']['comments']
        issue_data['Issue Comments'] = [
            {'Author': comment['author']['name'], 'Body': comment['body']}
            for comment in comments
        ]
    except KeyError:
        issue_data['Issue Comments'] = None

    try:
        #issue_data['Sprint'] = issue['fields']['customfield_10600']
        sprint = issue['fields']['customfield_10600']
        match = re.search(r"name=([^,]+)", sprint[0])
        if match:
            issue_data['Sprint'] = match.group(1)
    except KeyError:
        issue_data['Sprint'] = None

    filtered_issue_data = {k: v for k, v in issue_data.items() if v not in (None, [], {}, '', 'null')}

    # Convert the dictionary to a JSON object
    return filtered_issue_data

def get_jira_ticket(ISSUE_ID, folder):
    ISSUE_URL = os.getenv("JIRA_URL") + f"/rest/api/2/issue/{ISSUE_ID}"

    # List of fields to retrieve
    fields = [
        "project", 
        "key", 
        "summary", 
        "description",
        "issuetype", 
        "status", 
        "priority", 
        "resolution",
        "resolutiondate",
        "assignee", 
        "reporter", 
        "creator", 
        "created", 
        "updated", 
        "lastViewed", 
        "votes", 
        "watches", 
        "attachment", 
        "timetracking",
        "timeestimate", 
        "timespent", 
        "labels",
        "issuelinks", 
        "fixVersions", 
        "comment", 
        "customfield_10600" # sprint name
    ]

    # Request headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("JIRA_BEARER_TOKEN")
    }
    params = {
        "fields": ",".join(fields)  # Specify the fields to retrieve
    }

    # Make the API request
    response = requests.get(ISSUE_URL, headers=headers, params=params)

    filename = "jira_" + ISSUE_ID + '.json'
    # Check for a successful response
    if response.status_code == 200:
        issue = response.json()
        cleaned_data = remove_null_fields(issue)
        importatn_data = get_important_fields(cleaned_data)
        with open(filename, 'w') as json_file:
            json.dump(importatn_data, json_file, indent=4)
        os.system(f"mv jira_{ISSUE_ID}.json {folder}")

    else:
        print(f"Failed to fetch {filename}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    get_jira_ticket("AIGILE-36", "./trainingData/jira")