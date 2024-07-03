# Work with OpenAI API
## Assistants

### Setup OpenAI account
1. Create your account on [OpenAI](https://platform.openai.com/playground/).
2. Go to the [billing section](https://platform.openai.com/settings/organization/billing/overview) and add a payment method (the API won't work without it).
3. You will need to pay a minimum of $5 to start (info valid as of 06.2024).
4. Create a new project.
5. Create a new [API key](https://platform.openai.com/api-keys) for your project.
6. You can find information about limits and also set a monthly budget and notifications [here](https://platform.openai.com/settings/organization/limits).
7. Information about usage is available [here](https://platform.openai.com/usage).
8. Add information to the `.env.example` file and rename it to `.env`.

### Setup code
1. Create a `trainingData` folder and add files with context to this folder. [Supported files](https://platform.openai.com/docs/assistants/tools/file-search/supported-files).
2. Install `python3` and the `openai` library.
3. Create your assistant using `python ./assistants/create_assistant_with_context.py`. This will return an `assistant ID`.
4. Add (or update) your context using `python ./assistants/update_context.py <assistant ID>`.
5. Create a new thread (if required) using `python ./assistants/create_thread.py`.
6. Ask a question to the assistant using `python ./assistants/create_new_thread_with_existing_assistant.py <assistant ID> <thread_ID>`.
7. You can list your existing assistants using `python ./assistants/list.py`.

### Add integrations
#### Slack
I tested integration with Zapier, instructions [here](https://www.youtube.com/watch?v=kLkMC-ZIXq4).
![Slack integration](./pictures/Slack_integration.png)
![Slack result](./pictures/Slack_result.png)
Also, [PlugBear](https://plugbear.io/) can be used (not tested yet...).