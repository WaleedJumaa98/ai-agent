import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

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
# Now we can access `args.user_prompt`

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

test_text = client.models.generate_content(model="gemini-2.5-flash", contents=messages)


if test_text.usage_metadata is None:
    raise RuntimeError("Failed to get usage metadata.")

if args.verbose:
    print("User prompt:", args.user_prompt)
    print(f"Prompt tokens: {test_text.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {test_text.usage_metadata.candidates_token_count}")

print(test_text.text)
