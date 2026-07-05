import os
import shutil


def copy_files(src_dir, dest_dir,remove):

    if not os.path.exists(src_dir):
        raise ValueError(f"Source directory '{src_dir}' does not exist.")
           
    if remove:
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        

    for file in os.listdir(src_dir):
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dest_dir, file)

        if os.path.isfile(src_path):
            print(f"Copying {src_path} to {dest_path}")
            shutil.copy(src_path, dest_path)

        if os.path.isdir(src_path):
            print(f"Copying {src_path} to {dest_path}")
            copy_files(src_path, dest_path, False)