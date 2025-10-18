import os
def write_file(working_directory, file_path, content):
    base_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_path, file_path))

    if not (full_path.startswith(base_path + os.sep) or full_path == base_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path),exist_ok=True)

        if os.path.exists(full_path) and os.path.isdir(full_path):
            return f'Error: "{file_path}" is a directory, not a file'
            
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: can't write {e}"






