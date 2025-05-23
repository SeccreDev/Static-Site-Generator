import sys
from copy_directory import copy_source_to_directory
from page_generation import generate_pages_recursively

def main():
    """
    Main function that drives the static site generator.
    Copies static assets and generates HTML pages from markdown content.
    """
    static_directory = "./static"
    public_directory = "./docs"
    markdown_path = "./content"
    template_path = "./template.html"
    default_basepath = "/"

    # Allow an optional command-line argument for the base path
    if len(sys.argv) > 1:
        default_basepath = sys.argv[1]
    
    copy_source_to_directory(static_directory, public_directory)
    generate_pages_recursively(markdown_path, template_path, public_directory, default_basepath)

if __name__ == "__main__":
    main()