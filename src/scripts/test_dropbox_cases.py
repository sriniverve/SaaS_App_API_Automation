import src.libs.saas.drop_box as db
import os
import json


with open(os.path.abspath(os.path.join("..", "data/file_upload_list.json"))) as f:
    json_file_list = json.loads(f.read())



def main():
    dbx = db.authenticate_with_tokens()
    if dbx is not None:
        db.get_current_account_details(dbx)
        db.get_root_files_list(dbx)
        db.get_files_list(dbx, "/Videos")
        folder_id = db.file_metadata(dbx, "/Videos").id
        db.file_share_send_email(dbx, folder_id, "srini.verve@gmail.com")
        db.upload_file(dbx, upload_image_file, '/Pictures/Image_File.jpg')

        for item in range(len(json_file_list)):
            file = os.path.abspath(os.path.join("..", f'data/{json_file_list[item]["filename"]}'))
            db.upload_file(dbx, file, f'/{json_file_list[item]["filename"]}')

        for item in range(len(json_file_list)):
             db.file_delete(dbx, f'/{json_file_list[item]["filename"]}')


if __name__ == main():
    main()