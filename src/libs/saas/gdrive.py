from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from apiclient import errors
from apiclient import http
import json
import io


def login_with_oauth():
    """
    login to the drive using oauth credentials
    """
    creds = None
    SCOPES = 'https://www.googleapis.com/auth/drive'
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    try:
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                # print(vars(creds))
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.abspath(os.path.join('..', "credentials/credentials_gdrive.json")), SCOPES)
                    # '/Users/skilladi/Documents/PyCharm Projects/SaaS_App_API_Automation/src/credentials/credentials_gdrive.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        print("There seems to be a login error")
        print(e)
        return None


def login_fail_attempt(scope):
    creds = None
    SCOPES = scope
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    try:
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                write_content = str(token.read())
            with open("token_pickle_invalid", "w+") as f:
                f.write(write_content)

    except Exception as e:
        print(e)


def get_file_list(service):
    """get list of the files & folders in the drive.

    :arg
        service: Drive API service instance.
    :returns
        items: List of files & folders if present
        None: If no file is present
    """

    try:
        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return None
        else:
            return items

    except Exception as e:
        print("There seems to be a problem in reading the file list from the drive")
        print(e)
        return None

def get_file_metadata(service, file_id):
    """get a file's metadata.

    :arg
        service: Drive API service instance.
        file_id: ID of the file to print metadata for
    :returns
        metadata of the file contents
    """

    try:
        file_metadata = service.files().get(fileId=file_id).execute()
        return file_metadata

    except Exception as e:
        print(f"An error occurred: {e}")


def get_file_content(service, file_id):
    """ to get a file's content
    :arg:
      service: Drive API service instance.
      file_id: ID of the file.
    :returns:
      File's content if successful, None otherwise.
    """
    try:
        file_content = service.files().get_media(fileId=file_id).execute()
        return file_content

    except Exception as e:
        print(f"An error occurred: {e}")


def is_folder(file_metadata):
    """To find out if it is a folder or a file.
    :arg:
      file_metadata   : file_metadata saved from the metadata request
    :returns:
      True: if it is a folder
      False: if it is a file
    """
    if file_metadata["mimeType"] == "application/vnd.google-apps.folder":
        return True
    else:
        return False


def download_file(service, file_id, filename):
    """Download a Drive file's content to the local filesystem.
    Args:
      service   : Drive API Service instance.
      file_id   : ID of the Drive file that will downloaded.
      local_fd  : io.Base or file object, the stream that the Drive file's contents will be written to.
    """
    fh = io.FileIO(filename, 'wb')
    request = service.files().get_media(fileId=file_id)
    media_request = http.MediaIoBaseDownload(fh, request)

    while True:
        try:
            download_progress, done = media_request.next_chunk()

        except Exception as e:
            print(f"An error occurred: {e}")

        if download_progress:
            print(f"Download Progress: {int(download_progress.progress() * 100)}")
        if done:
            print("Download Complete")
            break


def copy_file(service, origin_file_id, copy_title):
    """Copy an existing file.
    Args:
      service: Drive API service instance.
      origin_file_id: ID of the origin file to copy.
      copy_title: Title of the copy.

    Returns:
      The copied file if successful, None otherwise.
    """
    copied_file = {"name" : copy_title}
    try:
        copy_status = service.files().copy(fileId=origin_file_id, body=copied_file).execute()
        return copy_status

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
