import os
from config import MAX_CHARS
#MAX_CHARS = 10000

def get_files_info(working_directory, directory="."):
    base_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_path, directory))

    if not (full_path.startswith(base_path + os.sep) or full_path == base_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    try:
        contents = []
        for content in os.listdir(full_path):
            path = os.path.join(full_path, content)
            contents.append( f"- {content}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}")
        return "\n".join(contents)
    except Exception as e:
        return f"Error: finding file content {e}"

def get_file_content(working_directory, file_path):
    base_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_path, file_path))

    if not (full_path.startswith(base_path + os.sep) or full_path == base_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, "r") as f:
            contents = f.read(MAX_CHARS)
            if len(contents)==MAX_CHARS:
                contents = contents + f'[...File "{file_path}" truncated at 10000 characters].'
        return contents
    except Exception as e:
        return f"Error: reading file content {e}"

    



    