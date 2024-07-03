# Work with Google Gemini API
1. Check the [cookbook](https://github.com/google-gemini/cookbook/tree/main?tab=readme-ov-file).

2. Access the [Google AI Studio](https://aistudio.google.com/app/apikey).

3. Google Gemini is available only in certain [locations](https://ai.google.dev/gemini-api/docs/available-regions). If your country is not on this list or doesn't have a trial period, you can use a VPN to change your location.

4. Update the .env.example file and then run `cp .env.example .env`.

## Usage
`python ./gemini/work_with_files.py` - Start a new prompt with a file.
`python ./delete_all_downloaded_files.py` - Delete all downloaded files.

## Files
The File API lets you store up to 20GB of files per project, with each file not exceeding 2GB in size. Files are stored for 48 hours and can be accessed with your API key for generation within that time period. It is available at no cost in all regions where the Gemini API is available.

[Files format](https://ai.google.dev/gemini-api/docs/prompting_with_media?lang=python#supported_file_formats)

[Available models and languages](https://ai.google.dev/gemini-api/docs/models/gemini#gemini-1.5-pro)
