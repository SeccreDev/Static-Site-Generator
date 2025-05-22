import os
import shutil
from blocks import markdown_to_html_node
from copy_directory import copy_source_to_directory, file_mover

def generate_pages_recursively(from_path, template_path, dest_path, basepath):
    static_contents = os.listdir(from_path)
    # Debugging purposes
    # print(f"Files inside the {source_directory} directory: {static_contents}")
    # End
    for content in static_contents:
        content_path = os.path.join(from_path, content)
        is_a_file = os.path.isfile(content_path)
        if (is_a_file):
            generate_page(content_path, template_path, dest_path, basepath)
            # Debugging purposes
            # print(f"Successfully copied {content} to {destination_directory} directory")
            # End 
        else:
            destination_directory = os.path.join(dest_path, content)
            os.mkdir(destination_directory)
            # Debugging purposes
            # print(f"Successfully created {destination_directory} directory")
            # End
            generate_pages_recursively(content_path, template_path, destination_directory, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
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
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
