import os
import shutil
from blocks import markdown_to_html_node
from copy_directory import copy_source_to_directory

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    file = open(from_path, 'r')
    markdown = file.read()
    file.close()

    file = open(template_path, 'r')
    template = file.read()
    file.close()

    title = extract_title(markdown)
    html_string = markdown_to_html_node(markdown).to_html()
    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
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
