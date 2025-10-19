import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    system_prompt = """You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    You should investiagte directories, files and content in the working directory to determine what they user reuires and perform actions to fulfill the user requests
    """
    load_dotenv('api_key.env')
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv)<2:
        print("Please provide prompt")
        sys.exit(1)

    verbose = "--verbose" in sys.argv

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    args = sys.argv[1:]
    user_prompt = " ".join(args)
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(20):

        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages, 
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        metadata = response.usage_metadata
        
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {metadata.prompt_token_count}")
            print(f"Response tokens: {metadata.candidates_token_count}")
        '''
        else:
            print(f"{response.text}")
        '''
        function_responses = []
        function_calls = response.function_calls
        if function_calls:
            for function_call_part in function_calls:
                function_call_result = call_function(function_call_part,verbose)
                if (not function_call_result.parts or not function_call_result.parts[0].function_response):
                    raise Exception("empty function call result")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
        if function_responses:        
            for result in function_responses:
                function_responses_message = types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name = result.function_response.name,
                            response= result.function_response.response
                        )
                    ],
                )
                messages.append(function_responses_message)
        if not function_calls:
            print(f"{response.text}")
            break

if __name__ == "__main__":
    main()