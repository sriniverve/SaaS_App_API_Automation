import src.libs.saas.amazonS3 as s3
import os
import json


with open(os.path.abspath(os.path.join("..", "data/file_upload_list.json"))) as f:
    json_file_list = json.loads(f.read())


def main():

    client = s3.oauth_login()

    s3.get_bucket_list(client)

    s3.create_bucket(client, "srininew", region="ap-south-1")
    s3.get_bucket_list(client)
    s3.delete_bucket(client, "srininew")
    s3.get_bucket_list(client)
    s3.get_bucket_permissions(client, 'srinivideos')
    file = os.path.abspath(os.path.join("..", f'data/{json_file_list[1]["filename"]}'))

    s3.delete_file(client, json_file_list[1]["filename"], 'srinidocuments')
    s3.upload_file(client, file, 'srinidocuments', object_name=json_file_list[1]["filename"])
    s3.download_file(client, 'pdf_doc.pdf', 'srinidocuments', 'PDF_Document.pdf')
    s3.modify_bucket_permissions(client, 'sriniimages', 'WRITE')
    s3.get_file_permissions(client, 'srinivideos', 'EtherChannel.mp4')
    s3.modify_file_permissions(client, 'srinivideos', 'EtherChannel.mp4','WRITE')
    s3.get_file_details(client, 'srinidocuments', 'Word_Document.docx')

if __name__ == '__main__':
    main()




