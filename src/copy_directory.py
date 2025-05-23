import os
import shutil

def copy_source_to_directory(source_directory, destination_directory): 
    """
    Copies the contents of source_dir into dest_dir.
    If dest_dir exists, it is deleted and recreated.

    Args:
        source_dir (str): Path to the source directory.
        dest_dir (str): Path to the destination directory.
    """
    path_purger(destination_directory)
    file_mover(source_directory, destination_directory)

def path_purger(path):
    """
    Deletes the directory if it exists, otherwise creates it.

    Args:
        path (str): Directory path to purge or create.
    """
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
    else:
        shutil.rmtree(path)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

def file_mover(source_directory, destination_directory):
    """
    Recursively copies files and directories from source_dir to dest_dir.

    Args:
        source_dir (str): Source path to copy from.
        dest_dir (str): Destination path to copy to.
    """
    static_contents = os.listdir(source_directory)
    for content in static_contents:
        content_path = os.path.join(source_directory, content)
        is_a_file = os.path.isfile(content_path)
        if (is_a_file):
            shutil.copy(content_path, destination_directory)
        else:
            destination_directory = os.path.join(destination_directory, content)
            os.mkdir(destination_directory)
            file_mover(content_path, destination_directory)