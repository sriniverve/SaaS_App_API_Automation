import dropbox
import os
import json


creds_file = os.path.abspath(os.path.join('..', "credentials/credentials_dropbox.json"))

with open(creds_file, "r") as f:
    json_data = json.loads(f.read())


def authenticate_with_tokens():
    """Authentication with tokens
       :arg
         token: Token extracted from the creds_file

       :returns
         dbx: dropbox session instance
       """

    try:
        dbx = dropbox.Dropbox(json_data["AccessToken"])
        return dbx

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def get_current_account_details(dbx):
    """To get the current account details
       :arg
         dbx: dropbox session instance

       :returns
         current_user: Object with current user details
       """

    try:
        current_user = dbx.users_get_current_account()
        print(vars(current_user))
        return current_user

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def get_root_files_list(dbx):
    """Entire list of files/folders in the root folder
       :arg
         dbx: dropbox session instance

       :returns
         list: files/folder list
       """

    try:
        for entry in dbx.files_list_folder('').entries:
            print(entry.name)

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def get_files_list(dbx, folder):
    """Entire list of files/folders in the root folder
       :arg
         dbx: dropbox session instance

       :returns
         list: files/folder list
       """

    try:
        for entry in dbx.files_list_folder(folder).entries:
            print(entry.name)

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def upload_file(dbx, source_file, dest_file):
    """Authentication with tokens
       :arg
         dbx: dropbox session instance

       :returns
         dbx: dropbox session instance
       """

    try:
        with open(source_file, "rb") as f:
            dbx.files_upload(f.read(), dest_file)

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def file_metadata(dbx, filename):
    """To get the metadata of a filename
       :arg
         dbx: dropbox session instance
         filename: full path of the file

       :returns
         file metadata
       """

    try:
        metadata = dbx.files_get_metadata(filename)
        print(metadata)
        return metadata
        #FileMetadata(name='PPP_3.mp4', id='id:vVKNQ8WCFVAAAAAAAAAAGw', client_modified=datetime.datetime(2020, 6, 9, 8, 47, 1),
        # server_modified=datetime.datetime(2020, 6, 18, 3, 24, 1), rev='015a8534ed3e67100000001d40353f0', size=21283100,
        # path_lower='/videos/ppp_3.mp4', path_display='/Videos/PPP_3.mp4', parent_shared_folder_id=None, media_info=None,
        # symlink_info=None, sharing_info=None, is_downloadable=True, export_info=None, property_groups=None,
        # has_explicit_shared_members=None, content_hash='850014e8740f3ec72d13bc8d8b15e28bb33ef990806ea90aea9e717b3dac1c05',
        # file_lock_info=None)

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def file_delete(dbx, filename):
    """To get the metadata of a filename
       :arg
         dbx: dropbox session instance
         filename: full path of the file

       :returns
         True: if it is successful
         False: if it fails to delete
       """

    try:
        dbx.files_delete(filename)


    except Exception as e:
        print(f"An error has occurred: {e}")
        return False


def file_share_send_email(dbx, folder_id, email):
    """To get the metadata of a filename
       :arg
         dbx: dropbox session instance
         filename: full path of the file

       :returns
         True: if it is successful
         False: if it fails to delete
       """

    try:
        member_selector = dropbox.sharing.MemberSelector.email(email)
        add_member = dropbox.sharing.AddMember(member_selector)
        members = [add_member]

        res = dbx.sharing_add_folder_member(folder_id, members)


    except Exception as e:
        print(f"An error has occurred: {e}")
        return False



