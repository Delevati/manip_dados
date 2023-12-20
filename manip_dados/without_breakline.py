import os 

def remove_newlines_from_text_files(folder_path):
    # Get a list of all files in the folder with a .txt extension
    txt_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]

    for file_name in txt_files:
        # Build the full path for the file
        file_path = os.path.join(folder_path, file_name)

        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Remove newline characters from the content
        modified_content = content.replace('\n', ' ')

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(modified_content)

remove_newlines_from_text_files('/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/port_vert-ground-truth')