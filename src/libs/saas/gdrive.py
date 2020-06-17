from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from apiclient import errors
from apiclient import http
from apiclient.http import MediaFileUpload
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

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.abspath(os.path.join('..', "credentials/credentials_gdrive.json")), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('drive', 'v3', credentials=creds)

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
        return service.files().get(fileId=file_id).execute()


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
        return service.files().get_media(fileId=file_id).execute()

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
    :arg
      service: Drive API service instance.
      origin_file_id: ID of the origin file to copy.
      copy_title: Title of the copy.

    :returns
      The copied file if successful, None otherwise.
    """
    copied_file = {"name" : copy_title}
    try:
        return service.files().copy(fileId=origin_file_id, body=copied_file).execute()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def delete_file(service, file_id):
    """Move a file to the trash.

    :arg
      service: Drive API service instance.
      file_id: ID of the file to trash.

    :returns
      The updated file if successful, None otherwise.
    """
    try:
        return service.files().delete(fileId=file_id).execute()
    except Exception as e:
        print(f"an error has occurred: {e}")
    return None


def upload_file(service, filename, filepath, mimetype):
    """Upload a file to the drive.

    :arg
      service: Drive API service instance.
      file_id: ID of the file to trash.

    :returns
      The updated file if successful, None otherwise.
    """

    try:
        file_metadata = {"name": filename}
        media = MediaFileUpload(f"{filepath}/{filename}", mimetype=mimetype)
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print("Upload successful")
        return file.get('id')

    except Exception as e:
        print(f"An error occurred: {e}")


def update_file(service, file_id, new_file_name, new_name, new_mime_type):
    """Update an existing file's metadata and content.

    :arg
      service: Drive API service instance.
      file_id: ID of the file to update.
      new_title: New title for the file.
      new_description: New description for the file.
      new_mime_type: New MIME type for the file.
      new_filename: Filename of the new content to upload.
      new_revision: Whether or not to create a new revision for this file.
    :returns
      Updated file metadata if successful, None otherwise.
    """

    try:
        # First retrieve the file from the API.
        file = service.files().get(fileId=file_id).execute()

        # File's new metadata.
        file["name"] = new_name
        file["description"] = new_description
        file["mimeType"] = new_mime_type

        # File's new content.
        media_body = MediaFileUpload(
            new_file_name, mimetype=new_mime_type, resumable=True)

        # Send the request to the API.
        updated_file = service.files().update(
            fileId=file_id,
            body=file,
            newRevision=new_revision,
            media_body=media_body).execute()
        return updated_file

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def rename_file(service, file_id, new_name):
    """Rename a file.

    :arg
      service: Drive API service instance.
      file_id: ID of the file to rename.
      new_title: New title for the file.
    :returns
      Updated file metadata if successful, None otherwise.
    """

    try:
        file = {"name": new_name}
        updated_file = service.files().update(fileId=file_id, body=file, fields="name").execute()
        return updated_file

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def insert_file(service, folder_id, mime_type, filename):
    """Insert new file.

    :arg
      service: Drive API service instance.
      title: Title of the file to insert, including the extension.
      description: Description of the file to insert.
      parent_id: Parent folder's ID.
      mime_type: MIME type of the file to insert.
      filename: Filename of the file to insert.
    :returns
      Inserted file metadata if successful, None otherwise.
    """

    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
        "name": filename,
        "mimeType": mime_type
    }

    # Set the parent folder
    if folder_id:
        body['parents'] = [{'id': folder_id}]

    try:
        return service.files().insert(body=body, media_body=media_body).execute()

    except Exception as e:
        print(f"an error has occurred: {e}")
        return None


def get_files_in_folder(service, folder_id):
    """Print files belonging to a folder.

    :arg
        service: Drive API service instance.
        folder_id: ID of the folder to print files from.
    :returns
        file_Id_list: Ids of the files present in the folder
    """

    page_token = None
    file_Id_list = []
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token

            children = service.children().list(folderId=folder_id, **param).execute()
            for child in children.get('items', []):
                print(child)
                print(f"file_Id_listFile {child['id']}")

            page_token = children.get('nextPageToken')
            if not page_token:
                break
        except Exception as e:
            print(f"an error has occurred: {e}")
            break


def find_folder_by_name(service, folder_name):
    """searches for folders for a given folder name

    :arg
        service: Drive API service instance.
        folder_name: Name of the folder to print files from.
    :returns
        folder_id: Id of the folder
    """

    try:
        page_token = None
        while True:
            response = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)',
                                                  pageToken=page_token).execute()

            for file in response.get('files', []):
                print(f"Found folder: {file.get('name')}, {file.get('id')}")
                if file.get('name') == folder_name:
                    return file.get('id')

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None