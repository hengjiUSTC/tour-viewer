from __future__ import print_function
import pickle
import os.path

from googleapiclient import http, errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
ROOT_DIR = "tourviewer"


class GoogleDriveClient:
    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'tv/static/tv/google_cred/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def download_file(self, file_id, local_fd):
        """Download a Drive file's content to the local filesystem.

        Args:
          file_id: ID of the Drive file that will downloaded.
          local_fd: io.Base or file object, the stream that the Drive file's
              contents will be written to.
        """
        request = self.service.files().get_media(fileId=file_id)
        media_request = http.MediaIoBaseDownload(local_fd, request)

        while True:
            try:
                download_progress, done = media_request.next_chunk()
            except errors.HttpError as error:
                print('An error occurred: %s' % error)
                return
            if download_progress:
                print('Download Progress: %d%%' % int(download_progress.progress() * 100))
            if done:
                print('Download Complete')
                return

    def list_dir(self, id="11pz9IQw679_9yz7ur7YzedQ4FRfKzBQM"):
        """
        list all dir
        """
        id = "'" + id + "'"

        # Call the Drive v3 API
        results = self.service.files().list(
            q=id + " in parents",
            pageSize=10).execute()
        items = results.get('files', [])

        return items