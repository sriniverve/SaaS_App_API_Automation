from __future__ import print_function
import os.path
import json
import src.libs.saas.gdrive as saas

# If modifying these scopes, delete the file token.pickle.


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    fname = os.path.abspath(os.path.join('..', "data/file_upload_list.json"))
    local_download_path = os.path.abspath(os.path.join('..', "data"))

    # with open(fname, "r") as f:
    #     json_list = json.loads(f.read())
    # print(json_list)
    # fail_attempt = saas.login_fail_attempt("https://www.googleapis.com/auth/drive")
    service = saas.login_with_oauth()
    if service is not None:
        print("Login to the gdrive successful")
        list_of_files = saas.get_file_list(service)
        print(list_of_files)
        if list_of_files is not None:
            for item in range(len(list_of_files)):
                fileID = list_of_files[item]["id"]
                file_metadata = saas.get_file_metadata(service,fileID)
                if file_metadata is not None:
                    if not saas.is_folder(file_metadata):
                        if file_metadata["mimeType"] == "video/mp4":
                            # newFileId = saas.copy_file(service, fileID, "new_file.mp4")
                            # if newFileId is not None:
                            #     print("copy successful")
                            if saas.download_file(service, fileID, f"{local_download_path}/{file_metadata['name']}") is not None:
                                print(download_status)
                        else:
                            print("Not a video file")
                        break

                    else:
                        print("this is a folder")


if __name__ == '__main__':
    main()