import os
import shutil
from blocks import markdown_to_html_node
from copy_directory import copy_source_to_directory, file_mover

def generate_pages_recursively(from_path, template_path, dest_path, basepath):
    """
    Recursively generates HTML pages from markdown files in a source directory.

    Args:
        from_path (str): The current directory to read markdown files from.
        template_path (str): The path to the HTML template.
        dest_path (str): The output directory where HTML files are written.
        base_path (str): Base URL path used for link rewriting.
    """
    static_contents = os.listdir(from_path)
    for content in static_contents:
        content_path = os.path.join(from_path, content)
        is_a_file = os.path.isfile(content_path)
        if (is_a_file):
            generate_page(content_path, template_path, dest_path, basepath)
        else:
            destination_directory = os.path.join(dest_path, content)
            os.mkdir(destination_directory)
            generate_pages_recursively(content_path, template_path, destination_directory, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    """
    Generates a single HTML page from a markdown file using a template.

    Args:
        from_path (str): Path to the markdown file.
        template_path (str): Path to the HTML template file.
        dest_path (str): Directory where the HTML file should be written.
        base_path (str): Base path used to update relative links in HTML.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    file = open(from_path, 'r')
    markdown = file.read()
    file.close()

    file = open(template_path, 'r')
    template = file.read()
    file.close()

    title = extract_title(markdown)
    html_string = markdown_to_html_node(markdown).to_html()
    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace('href="/', 'href="' + basepath).replace('src="/', 'src="' + basepath)
    
    if os.path.exists(dest_path):
        filename = "index.html"
        path = os.path.join(dest_path, filename)
        contents = os.listdir(dest_path)

        if filename in contents:
            os.remove(path)

        file = open(path, 'w')
        file.write(html_page)
        file.close()

    else:
        print(f"Create the {dest_path} directory first!")
        
def extract_title(markdown):
    """
    Extracts the title from a markdown string (assumes the first H1 is the title).

    Args:
        markdown (str): Markdown content.

    Returns:
        str: The extracted title.

    Raises:
        ValueError: If no H1 title is found.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
