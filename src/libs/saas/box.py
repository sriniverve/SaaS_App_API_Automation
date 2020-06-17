from boxsdk import Client, OAuth2


def get_user_details(client):
    """get info on the current authenticated user
    :arg
      client: Box API service instance.

    :returns
      ID of the user
    """

    try:
        return client.user(user_id='me').get(fields=['login'])
        # print(f"The email of the user is: {me['login']}")

    except Exception as e:
        print(f"Error has occurred: {e}")
        return None


def get_root_folder_details(client):
    """Get the id of the given folder
    :arg
      client: Box API service instance

    :returns
      ID of the folder name
    """
    try:
        root_folder = client.folder(folder_id='0').get()
        print(f"The root folder is owned by: {root_folder.owned_by['login']}")
        items = root_folder.get_items(limit=100, offset=0)
        print('This is the first 100 items in the root folder:')
        for item in items:
            print("   " + item.name, item.id)

    except Exception as e:
        print(f"Error has occurred: {e}")
        return None


def get_folder_by_name(client, folder_name):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_name: Name of the folder

    :returns
      ID of the folder name
    """
    try:
        root_folder = client.folder(folder_id='0').get()
        items = root_folder.get_items(limit=100, offset=0)
        for item in items:
            if item.name == folder_name:
                return item.id

    except Exception as e:
        print(f"Error has occurred: {e}")
        return None


def get_files_in_folder(client, folder_id):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_id: Id of the folder

    :returns
      Contents of the folder
    """

    try:
        items = client.folder(folder_id=folder_id).get_items()
        for item in items:
            print(item.name, item.id)
        return items
    except Exception as e:
        print(f"An error has occurred: {e}")


def create_folder(client, parent_folder_id, folder_name):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_id: Id of the folder

    :returns
      Contents of the folder
    """

    try:
        subfolder = client.folder(parent_folder_id).create_subfolder(folder_name)
        print(f'Created subfolder with ID {subfolder.id}')

    except Exception as e:
        print(f"An error occurred: {e}")


def get_file_by_name(client, folder_id, file_name):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_id: Id of the folder

    :returns
      Contents of the folder
    """

    try:
        items = client.folder(folder_id=folder_id).get_items()
        for item in items:
            if item.name == file_name:
                return item.id
        return "Did not find the file"

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def upload_file(client, folder_id, file_name):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_id: Id of the folder
      file_name: filename to be uploaded
      
    :returns
    """

    new_file = client.folder(folder_id).upload(file_name)
    print(f"File {new_file.name} uploaded to Box with file ID {new_file.id}")
    return new_file.id
        

def download_file(client, file_id):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_id: Id of the folder

    :returns
      Contents of the folder
    """

    file_content = client.file(file_id).content()
    print(file_content)


def delete_file(client, file_id):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      file_id: Id of the file

    :returns
      True: if successful
      False: if not successful
    """

    try:
        client.file(file_id=file_id).delete()
        print(f"File with {file_id} has been deleted")
        return True

    except Exception as e:
        print(f"an error has occurred: {e}")
        return False


def update_file(client, file_id, new_name):
    """Renaming the file
    :arg
      client: Box API service instance
      file_id: Id of the file

    :returns
      True: if successful
      False: if not successful
    """

    try:
        updated_file = client.file(file_id).update_info({'name': new_name})
        print(f"{file_id} is successfully renamed to {new_name}")

    except Exception as e:
        print(f"an error has occurred: {e}")
        return None

# def is_file_exists(client, file_id):
#     """Validate if the file exists
#     :arg
#       client: Box API service instance
#       file_id: Id of the file
#
#     :returns
#       True: if successful
#       False: if not successful
#     """
#     try:
#         file_info = client.file(file_id).get()
#         return True
#
#     except Exception as e:
#         print("File not present")
#         return False


def folder_collaborations(client, folder_id):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_id: Id of the folder

    :returns
      Contents of the folder
    """

    try:
        collaborations = client.folder(folder_id=folder_id).get_collaborations()
        print(collaborations)
        for collab in collaborations:
            target = collab.accessible_by
            print(f'{target.type.capitalize()} {target.name} is collaborated on the folder')
    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def get_collections(client):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_id: Id of the folder

    :returns
      Contents of the folder
    """

    try:
        collections = client.collections()
        for collection in collections:
            # print(f'Collection "{collection.name}" has ID {collection.id}')
            return collection.name, collection.id

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def get_collection_items(client, collection_id):
    """Get the id of the given folder
    :arg
      client: Box API service instance
      folder_id: Id of the folder

    :returns
      Contents of the folder
    """

    try:
        items = client.collection(collection_id=collection_id).get_items()
        for item in items:
            print('{item.type.capitalize()} "{item.name}" is in the collection')

    except Exception as e:
        print(f"An error has occurred: {e}")
        return None
