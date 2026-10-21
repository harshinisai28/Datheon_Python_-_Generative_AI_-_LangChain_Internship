
# Astra – Multi-Tool Autonomous AI Agent

## Overview

Astra is a Python-based interactive AI agent demonstration.
It uses specialized tools to perform calculations, retrieve the
current date and time, and analyze text through a Streamlit interface.

## Features

- Calculator for arithmetic expressions
- Current date and time
- Text analysis and word frequency
- Interactive chat interface
- Chat history during the current session
- Clear chat option
- Readable, responsive dashboard
- No external AI API key required

## Technologies

- Python
- Streamlit
- Python AST module
- Regular expressions
- Collections and datetime modules

## Project Structure

task3_AI_Agent/
├── main.py
├── tools.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore

## Installation

1. Install Python 3.12.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Install the required package:

   python -m pip install -r requirements.txt

## Run the Application

python -m streamlit run main.py

The application will open in your browser.

## Example Commands

- calculate 25 * 4
- calculate (10 + 5) / 3
- What is the current time?
- analyze: Python is easy to learn.
- help

## How It Works

1. The user enters a command or message.
2. Astra identifies supported commands using simple rules.
3. The appropriate Python tool processes the request.
4. The result is displayed in the Streamlit interface.

## Limitations

This is a local, rule-based AI agent demonstration.
It does not use a large language model or external AI API.
General questions outside its supported commands receive a
helpful message describing the available functionality.

## Conclusion

Astra demonstrates how Python tools can be combined with a
Streamlit interface to build a simple, interactive multi-tool agent.
