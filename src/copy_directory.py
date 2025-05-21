import os
import shutil

def copy_source_to_directory(source_directory, destination_directory): 
    # Creates public directory if it does not exist. Purges if it exists
    path_purger(destination_directory)

    # Copies all the files from static directory to the newly created public directory
    file_mover(source_directory, destination_directory)

def path_purger(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
            # Debugging purposes
            # print("Directory 'public' created")
            # End
        except OSError as error:
            print(error)
    else:
        shutil.rmtree(path)
        try:
            os.mkdir(path)
            # Debugging purposes
            # print("Directory 'public' purged")
            # End
        except OSError as error:
            print(error)

def file_mover(source_directory, destination_directory):
    static_contents = os.listdir(source_directory)
    # Debugging purposes
    # print(f"Files inside the {source_directory} directory: {static_contents}")
    # End
    for content in static_contents:
        content_path = os.path.join(source_directory, content)
        is_a_file = os.path.isfile(content_path)
        if (is_a_file):
            shutil.copy(content_path, destination_directory)
            # Debugging purposes
            # print(f"Successfully copied {content} to {destination_directory} directory")
            # End 
        else:
            destination_directory = os.path.join(destination_directory, content)
            os.mkdir(destination_directory)
            # Debugging purposes
            # print(f"Successfully created {destination_directory} directory")
            # End
            file_mover(content_path, destination_directory)