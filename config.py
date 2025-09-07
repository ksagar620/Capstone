import os
from dotenv import load_dotenv

load_dotenv()
domain = os.getenv("domain")
username = os.getenv("username")
pwd = os.getenv("pws")
Refernece_folder_url = os.getenv("Refernece_folder_url")
local_directory = os.getenv("local_directory")
Target_Archive_Folder = os.getenv("Target_Archive_Folder")
Folder_Name = os.getenv("Folder_Name")
embedding_model = os.getenv("embedding_model")
GPT_model = os.getenv("GPT_model")
tesseract_cmd = os.getenv("tesseract_cmd")