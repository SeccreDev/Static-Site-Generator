from copy_directory import copy_source_to_directory
from page_generation import generate_page

def main():
    static_directory = "./static"
    public_directory = "./public"
    markdown_path = "./content/index.md"
    template_path = "./template.html"

    copy_source_to_directory(static_directory, public_directory)
    generate_page(markdown_path, template_path, public_directory)

if __name__ == "__main__":
    main()