# Working with the OpenAI API

## Assistants

### Setting Up an OpenAI Account

1. Create your account on [OpenAI](https://platform.openai.com/playground/).
2. Go to the [billing section](https://platform.openai.com/settings/organization/billing/overview) and add a payment method (the API won't work without it).
3. You will need to pay a minimum of $5 to start (information valid as of 06.2024).
4. Create a new project.
5. Create a new [API key](https://platform.openai.com/api-keys) for your project.
6. You can find information about limits and set a monthly budget and notifications [here](https://platform.openai.com/settings/organization/limits).
7. Information about usage is available [here](https://platform.openai.com/usage).

### Setting Up the Code

1. Use the code in the `AI_integrations` folder to add content for model learning from Confluence and Jira.
2. Install libraries from `requirements.txt`.
3. Update the configuration in [.env.example](./.env.example) and run `cp ./.env.example ./.env`.
4. Create your assistant using `python ./OpenAI/assistants/create_assistant.py`. This will return an `Assistant ID` and `Vector Store ID` assigned to the assistant.
5. Add (or update) assistant content using `python ./OpenAI/assistants/update_content.py <Vector Store ID>`.
6. Update the assistant using `python ./OpenAI/assistants/update_assistant.py <Assistant ID>`.
7. Delete the assistant and all resources not used by other assistants: `python ./OpenAI/assistants/delete_assistant.py <Assistant ID>`.
8. Delete all files from OpenAI (if you downloaded them manually): `python ./OpenAI/assistants/delete_all_files.py`.

#### Create Assistant

`python ./OpenAI/assistants/create_assistant.py`

#### Update Assistant

`python ./OpenAI/assistants/update_assistant.py <Assistant ID>`

#### Update Knowledge Base

`python ./AI_integrations/jira/main.py`  
`python ./AI_integrations/confluence/main.py`  
`python ./OpenAI/assistants/update_content.py <Vector Store ID>`

#### Delete Assistant (and all unused vector stores and files)

`python ./OpenAI/assistants/delete_assistant.py <Assistant ID>`

### Legacy

1. Add (or update) your context using `python ./OpenAI/assistants_legacy/update_context.py <Assistant ID>`.
2. Create a new thread (if required) using `python ./OpenAI/assistants_legacy/create_thread.py`.
3. Ask a question to the assistant using `python ./OpenAI/assistants_legacy/create_new_thread_with_existing_assistant.py <Assistant ID> <Thread ID>`.
4. List your existing assistants using `python ./OpenAI/assistants_legacy/list.py`.

### Adding Integrations

#### Slack

I tested the integration with Zapier. Instructions can be found [here](https://www.youtube.com/watch?v=kLkMC-ZIXq4).  
![Slack integration](./pictures/Slack_integration.png)
![Slack result](./pictures/Slack_result.png)  
You can also use [PlugBear](https://plugbear.io/) (not tested yet).