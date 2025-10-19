import os
from google import genai
from google.genai import types

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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)



    