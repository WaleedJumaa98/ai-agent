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

if args.verbose:
    print(f"User prompt: {args.user_prompt}")

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

for _ in range(20):
    test_text = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if test_text.candidates:
        for candidate in test_text.candidates:
            messages.append(candidate.content)

    if args.verbose and test_text.usage_metadata:
        print(f"Prompt tokens: {test_text.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {test_text.usage_metadata.candidates_token_count}")

    if not test_text.function_calls:
        print("Final response:")
        print(test_text.text)
        break

    function_responses = []
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
        function_responses.append(function_call_result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))

else:
    print("Max iterations reached without a final response.")
    exit(1)
