import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    base_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_path, file_path))

    if not (full_path.startswith(base_path + os.sep) or full_path == base_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith("py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        run_args = ["python3",f"{full_path}"]
        for arg in args:
            run_args.append(arg)

        object = subprocess.run(run_args, capture_output = True,timeout=30,text = True,)

        output = f"STDOUT: {object.stdout}"
        error = f"STDERR: {object.stderr}"
        string_object = output +" "+ error
        if len(object.stdout)==0 and len(object.stderr)==0:
            return "No output produced"
        if object.returncode  != 0:
            return f"Error: Process exited with code {object.returncode}"
        return string_object
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description= "execute a Python file and return its stdout/stderr; use this to run .py files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that can be executed, relative to the working directory.",
            ),
        },
    ),
)