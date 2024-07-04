# This repository contains examples of working with different AI tools
## The main point is to check how we can upload our own files to an API for updating the AI knowledge base.
## OpenAI
`cd ./OpenAI/`  
[OpenAI readme](./OpenAI/Readme.md)

## Google Gemini
`cd ./gemini/`  
[Gemini readme](./Gemini/Readme.md)

## Integrations
### Jira (In progress)
1. Create your own Jira API token [here](https://jira.ontrq.com/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens)
1. Update info in `./AI_integrations/jira/.env.example` and `cp ./AI_integrations/jira/.env.example ./AI_integrations/jira/.env`
2. run `python ./AI_integrations/jira/get_tickets_from_jira.py`

## TODO:
1. create data flow diagram
2. add requirements.txt to both Readme files
3. create instruction for assistant for work with Jira JSON format