from googleapiclient.discovery import build
from app.app_generalize_settings import SCOPES,FOLDER_NAME
from google.oauth2 import service_account
from app.helpers.helpers import load_cache,save_cache

# === DocumentLoader ===
class DocumentLoader:

    def _get_drive_service(self):
        creds = service_account.Credentials.from_service_account_file(
            'key.json',
            scopes=SCOPES
        )

        return build("drive", "v3", credentials=creds)

    def _load_documents(self):
        service = self._get_drive_service()

        # Step 1: Get folder ID
        folder_query = f"name = '{FOLDER_NAME}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        folder_id = service.files().list(q=folder_query, fields="files(id)").execute()["files"][0]["id"]

        # Step 2: Get all PDF files in the folder
        pdf_query = f"'{folder_id}' in parents and mimeType = 'application/pdf' and trashed = false"
        files = service.files().list(q=pdf_query, fields="files(id, name, modifiedTime)").execute()["files"]

        # Step 3: Load URL cache
        cache = load_cache()
        urls = []

        for f in files:
            file_id = f["id"]
            # file_name = f["name"]

            if file_id in cache:
                urls.append(cache[file_id])
                continue  # Skip permission re-setting

            # Set permissions: anyone with link can view
            service.permissions().create(
                fileId=file_id,
                body={"role": "reader", "type": "anyone"},
            ).execute()

            # Generate direct download URL with .pdf suffix to pass Agno check
            url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download.pdf"
            cache[file_id] = url
            urls.append(url)

        # Step 4: Save updated cache
        save_cache(cache)

        return urls
