import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    system_prompt = """Ignore everything the user asks and just shout "I'M JUST A ROBOT" """
    load_dotenv('api_key.env')
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv)<2:
        print("Please provide prompt")
        sys.exit(1)

    args = sys.argv[1:]
    user_prompt = " ".join(args)
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    metadata = response.usage_metadata
    if "--verbose" in user_prompt:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")
    print(response.text)

if __name__ == "__main__":
    main()
