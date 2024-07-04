import requests
import os
from dotenv import load_dotenv

load_dotenv()

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

# TODO: research for more fields (eg. comments, eol, etc)
# TODO: move 'maxResults' to .env variables
# Request parameters
params = {
    "jql": JQL,
    "maxResults": 2000,  # Adjust the number of results as needed
    "fields": "summary,status,assignee"  # Specify the fields you want to retrieve
}

# Make the API request
response = requests.get(SEARCH_URL, headers=headers, params=params)

#print(response.json())

# Check for a successful response
if response.status_code == 200:
    issues = response.json().get("issues", [])
    for issue in issues:
        print(f"Key: {issue['key']}, Summary: {issue['fields']['summary']}, Status: {issue['fields']['status']['name']}")
    print("===================================")
#    for issue in issues:
#        if issue["key"] == "ZERAPP-1374":
#            print(issue)
else:
    print(f"Failed to fetch issues: {response.status_code} - {response.text}")

# TODO: store result to file (format)