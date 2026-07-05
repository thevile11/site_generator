from textnode import TextType,TextNode
from copy_files import copy_files
from gencontent import generate_page,generate_pages_recursive
import sys



def main():
    
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    src_dir = "static"
    dest_dir = "public"
    copy_files(src_dir,dest_dir,True)
    generate_pages_recursive("content", "template.html", "docs", basepath)




main()