import os
from config import MAX_CHARS
from google import genai
from google.genai import types

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
                contents = contents + f'[...File "{file_path}" truncated at {MAX_CHARS} characters].'
        return contents
    except Exception as e:
        return f"Error: reading file content {e}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a file, at the specified path relative to the working directory, truncated to a maximum character count, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The content of a file, at the specified path relative to the working directory.",
            ),
        },
    ),
)