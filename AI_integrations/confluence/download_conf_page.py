import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv(os.path.dirname(os.path.abspath(__file__)) + "/../../OpenAI/.env")

def get_page(base_url, username, password, page_id, page_title, folder):

    endpoint = f'/spaces/flyingpdf/pdfpageexport.action?pageId={page_id}'

    # Make the request
    response = requests.get(base_url + endpoint, auth=HTTPBasicAuth(username, password), stream=True)

    # Check the response status
    if response.status_code == 200:
        print("Request was successful")
        pdf_filename = f"confluence_{page_title}.pdf"
        with open(pdf_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Page content saved as {pdf_filename}")
        os.system(f"mv {pdf_filename} {folder}")
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Replace with your Confluence base URL, username, and password
    base_url = os.getenv("CONFLUENCE_BASE_URL")
    username = os.getenv("CONFLUENCE_USERNAME")
    password = os.getenv("CONFLUENCE_PASSWORD")
    page_id = "508920206"
    get_page(base_url, username, password, page_id, "test", './')