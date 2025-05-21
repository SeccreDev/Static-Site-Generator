from copy_directory import copy_source_to_directory

def main():
    source_directory = "./static"
    destination_directory = "./public"
    copy_source_to_directory(source_directory, destination_directory)

if __name__ == "__main__":
    main()