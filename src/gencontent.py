import os
from pathlib import Path
from markdown_blocks import markdown_to_blocks,markdown_to_html_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("# "):
            text = block[1:].strip()
            return text

    raise ValueError("Missing h1 header")
    



def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    src_file = open(from_path, "r")
    md = src_file.read()
    src_file.close()

    tmpl_file = open(template_path, "r")
    template = tmpl_file.read()
    tmpl_file.close()
    html_str = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    new_tmpl=template.replace("{{ Title }}", title).replace("{{ Content }}", html_str).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/",f"src=\"{basepath}")

    dirs = os.path.dirname(dest_path)
    if dirs != "":
        os.makedirs(dirs,exist_ok=True)
    dest_file= open(dest_path, "w")
    dest_file.write(new_tmpl)
    dest_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Processing: {dir_path_content}")
    dirs = os.listdir(dir_path_content)

    for content in dirs:
        full_path= os.path.join(dir_path_content,content)
        new_dest = os.path.join(dest_dir_path,content)
        if os.path.isfile(full_path):
            generate_page(full_path,template_path,Path(new_dest).with_suffix(".html"),basepath)
        else:
            generate_pages_recursive(full_path,template_path,new_dest,basepath)