import os
import shutil

from blocks import extract_title, markdown_to_html_node


def clean_copy(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    def recursive_copy(source, destination):
        for item in os.listdir(source):
            src_path = os.path.join(source, item)
            dest_path = os.path.join(destination, item)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
                print(f"copied file: {src_path} -> {dest_path}")
            else:
                os.mkdir(dest_path)
                print(f"created directory: {dest_path}/")
                recursive_copy(src_path, dest_path)

    recursive_copy(source, destination)


def read_if_valid(path):
    if not os.path.exists(path):
        raise ValueError(f"path {path} does not exist")
    if not os.path.isfile(path):
        raise ValueError(f"path {path} is not a file")

    with open(path, "r") as file:
        return file.read()


def generate_page(src_path, template_path, dest_path):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")
    md_file = read_if_valid(src_path)
    tmpl_file = read_if_valid(template_path)
    content = markdown_to_html_node(md_file).to_html()
    title = extract_title(md_file)

    final_html = tmpl_file.replace("{{ Title }}", title).replace(
        "{{ Content }}", content
    )
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(final_html)
