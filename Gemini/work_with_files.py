import google.generativeai as genai
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    # Upload file
    sample_file = genai.upload_file(path=os.getenv("FILE_PATH"), display_name=os.getenv("FILE_DISPLAY_NAME"))
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}, file name {sample_file.name}")

    # test PDF upload
    #  500 An internal error has occurred. Please retry or report in https://developers.generativeai.google/guide/troubleshooting
    #sample_file = genai.upload_file(path="./trainingData_all/Copy_data_from_PROD_to_DEV_RDS.pdf", display_name="Sample markdown", mime_type="text/rtf")
    #print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}, file name {sample_file.name}")

    # get file
    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{sample_file.display_name}' as: {sample_file.uri}")

    try:
        model = genai.GenerativeModel(model_name=os.getenv("GEMIMI_MODEL"))

        # Pls provide instruction fro setup Open AI API, based on this file
        response = model.generate_content(
            [os.getenv("QUESTION"), file]
        )
        print(response.text)
    except Exception as error:
        print(f"Something goes wrong: {error}")
    finally:
        # Delete file
        genai.delete_file(sample_file.name)
        print(f"Deleted {sample_file.display_name}.")