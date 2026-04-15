# AI Agent

An AI-powered coding assistant that uses Google's Gemini API to perform file operations, execute Python code, and manage project files through natural language commands.

## Overview

This project implements an AI agent that can:
- List files and directories
- Read file contents
- Write or overwrite files
- Execute Python files with arguments

The agent uses function calling with Google's Gemini 2.5 Flash model to safely perform operations within a restricted working directory.

## Project Structure

```
ai-agent/
├── main.py                 # Main AI agent script
├── prompts.py              # System prompts for the AI
├── call_function.py        # Function calling dispatcher
├── pyproject.toml          # Project configuration
├── functions/              # Core function modules
│   ├── config.py          # Configuration constants
│   ├── get_files_info.py  # File listing functionality
│   ├── get_file_content.py # File reading functionality
│   ├── write_file.py      # File writing functionality
│   └── run_python_file.py # Python execution functionality
├── calculator/            # Example calculator application
│   ├── main.py           # Calculator CLI entry point
│   ├── tests.py          # Unit tests for calculator
│   ├── lorem.txt         # Sample text file
│   └── pkg/
│       ├── calculator.py # Calculator logic
│       ├── render.py     # JSON output formatting
│       └── morelorem.txt # Another sample file
└── test_*.py             # Test scripts for functions
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-agent
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
Create a `.env` file with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Running the AI Agent

The main script accepts a natural language prompt and uses AI to determine what file operations to perform:

```bash
python main.py "Read the calculator.py file and show me the evaluate method"
```

Add `--verbose` for detailed output:
```bash
python main.py "List all files in the calculator directory" --verbose
```

### Example Calculator App

The project includes a sample calculator application:

```bash
cd calculator
python main.py "3 + 5 * 2"
```

Output:
```json
{
  "expression": "3 + 5 * 2",
  "result": 13
}
```

Run tests:
```bash
python tests.py
```

## Core Functions

### File Operations

All functions operate within a restricted working directory (`./calculator` by default) for security.

- **get_files_info(directory)**: Lists files in a directory with size and type information
- **get_file_content(file_path)**: Reads file contents (truncated at 10,000 characters)
- **write_file(file_path, content)**: Writes or overwrites files
- **run_python_file(file_path, args)**: Executes Python files with optional arguments

### Security Features

- Path traversal protection prevents accessing files outside the working directory
- File operations are sandboxed to the calculator directory
- Python execution is limited to .py files with timeout protection

## Configuration

- **MAX_CHAR** (functions/config.py): Maximum characters to read from files (default: 10,000)
- Working directory is hardcoded to `./calculator` in call_function.py for security

## Testing

Run the test scripts to verify functionality:

```bash
python test_get_files_info.py
python test_get_file_content.py
python test_write_file.py
python test_run_python_file.py
```

## Dependencies

- `google-genai==1.12.1`: Google's Generative AI SDK
- `python-dotenv==1.1.0`: Environment variable management

## API Key Setup

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/) and set it in your `.env` file:

```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

## Security Warning

⚠️ **IMPORTANT**: This project is for educational purposes only and should not be used in production or given to others for practical use.

### Security Limitations

This AI agent implementation has several security and safety limitations:

- **Limited Sandboxing**: Operations are restricted to the `./calculator` directory, but within that directory, the agent can read, write, and execute arbitrary files
- **Python Code Execution**: The `run_python_file` function can execute any Python code within the working directory without restrictions
- **No Authentication**: Anyone with access to the script can run it and make requests to the Gemini API
- **API Key Exposure**: The Gemini API key is stored in environment variables and could be accessed by executed code
- **No Input Validation**: User prompts are passed directly to the AI model without additional filtering
- **Basic Path Protection**: While path traversal attacks are prevented, the sandbox boundaries could potentially be tested

### Intended Use

This project demonstrates:
- Function calling with Google's Gemini API
- Basic file operation sandboxing
- AI-powered coding assistance concepts

**Do not use this for:**
- Production applications
- Handling sensitive data
- Executing untrusted code
- Real-world file management

For production AI agents, consider additional security measures like:
- Comprehensive input sanitization
- Code review and approval workflows
- Restricted execution environments (containers, VMs)
- Proper authentication and authorization
- Audit logging
- Rate limiting and abuse prevention