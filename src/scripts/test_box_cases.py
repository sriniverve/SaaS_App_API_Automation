import src.libs.saas.box_auth as auth
import src.libs.saas.box as box
from boxsdk import Client, OAuth2
import os.path
import json


creds_file = os.path.abspath(os.path.join('..', "credentials/credentials_box.json"))
upload_file = os.path.abspath(os.path.join('..', "data/Word_Document.docx"))


def main():
    """Shows basic usage of the Drive v3 API.
    """

    with open(creds_file, 'r') as f:
        json_data = json.loads(f.read())

    if "AccessToken" and "RefreshToken" in json_data:
        oauth = auth.authenticate_with_tokens(json_data['ClientID'],
                                    json_data['ClientSecret'],
                                    json_data['AccessToken'],
                                    json_data['RefreshToken'])

    else:
        with open(creds_file, 'r') as f:
            json_data = json.loads(f.read())
        oauth, access_token, refresh_token = auth.authenticate_one_time()
        data = {"AccessToken": access_token, "RefreshToken" : refresh_token}
        json_data.update(data)
        with open(creds_file, 'w') as f:
            json.dump(json_data, f)

    client = Client(oauth)

    me = box.get_user_details(client)
    folder_list = box.get_root_folder_details(client)
    folder_id = box.get_folder_by_name(client, "Videos")
    box.get_files_in_folder(client, folder_id)
    file_id = box.get_file_by_name(client, folder_id, "PPP_3.mp4")
    print(f"File id of PPP_3.mp4 is {file_id}")
    folder_id2 = box.get_folder_by_name(client, "Documents")
    file_id2 = box.upload_file(client, folder_id2, upload_file)
    box.update_file(client, file_id2, 'ModifiedFile.docx')
    box.delete_file(client, file_id2)


if __name__ == '__main__':
    main()