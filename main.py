import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import call_function, available_functions

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found in environment variables. Please set it in api-key.env file."
    )
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

test_text = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

if test_text.usage_metadata is None:
    raise RuntimeError("Failed to get usage metadata.")

if args.verbose:
    print("User prompt:", args.user_prompt)
    print(f"Prompt tokens: {test_text.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {test_text.usage_metadata.candidates_token_count}")

if test_text.function_calls:
    for function_call in test_text.function_calls:
        function_call_result = call_function(function_call, verbose=args.verbose)
        if not function_call_result.parts:
            raise Exception("No parts in function call result")
        if function_call_result.parts[0].function_response is None:
            raise Exception("No function response in result")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("No response in function response")
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(test_text.text)
