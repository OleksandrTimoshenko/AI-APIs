# This repository contains examples of working with different AI tools
## The main point is to check how we can upload our own files to an API for updating the AI knowledge base.
## OpenAI 
[OpenAI readme](./OpenAI/Readme.md)

## Google Gemini  
[Gemini readme](./Gemini/Readme.md)

## Integrations
### Jira (In progress)
1. Create your own Jira API token [here](https://jira.ontrq.com/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens)
1. Update info in `./AI_integrations/jira/.env.example` and `cp ./AI_integrations/jira/.env.example ./AI_integrations/jira/.env`
2. run `python ./AI_integrations/jira/main.py`

### Confluence (In progress)
1. Update info in `./AI_integrations/confluence/.env.example` and `cp ./AI_integrations/confluence/.env.example ./AI_integrations/confluence/.env`
2. run `python ./AI_integrations/confluence/main.py`

## Project structure
```
├── AI_integrations
│   ├── confluence
│   └── jira
├── Gemini
├── OpenAI
├── Readme.md
└── trainingData
    └── jira
    │    ├── jira_SPACE-XXXX.json
    │    ...
    └── confluence
        ├── confluence_SPACE-docx-name.json
        ...
```

![Data flow structure](./images/OpenAI_assistant_data_flow.png)

## TODO:
1. create instruction for assistant for work with Jira JSON format
2. Update Jira structure?