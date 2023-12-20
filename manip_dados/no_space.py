 
import os 

def rename_files(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    for file_name in files:
        # Remove all special characters except '.' and '_'
        new_name = ''.join(c if c.isalnum() or c in ['.', '_'] else '_' for c in file_name)
        # Build the full paths for the old and new names
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)
        # Rename the file
        os.rename(old_path, new_path)

rename_files('/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/port_vert-ground-truth')