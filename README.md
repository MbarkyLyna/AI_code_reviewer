# AI Code Reviewer

A code analysis tool that uses Groq's LLM API to review code, find security vulnerabilities, and generate test cases. Built with Streamlit.

**Live Demo:** [https://aicodereviewer-mbarkylyna.streamlit.app/](https://aicodereviewer-mbarkylyna.streamlit.app/)

## What It Does

Paste code and get instant feedback on quality, security issues, and improvement suggestions. It analyzes:

- Code quality (syntax errors, bad practices, inefficient patterns)
- Security vulnerabilities (SQL injection, XSS, authentication issues)
- Test case generation (pytest/jest/junit)
- Refactored code suggestions

Uses Groq's Llama 3.1 8B model for fast analysis.

## Tech Stack

- Streamlit for the UI
- Groq API for LLM processing
- Python 3.8+


## Features

The `CodeReviewer` class has three main methods:

- `analyze_code()` - Scores code quality, identifies issues, suggests improvements
- `check_security()` - Scans for vulnerabilities specific to the submitted code
- `suggest_tests()` - Generates test cases with appropriate testing frameworks

Each method sends targeted prompts to Groq's API focusing on actionable feedback rather than generic advice.

## Limitations

- 10,000 character code limit
- Analysis quality depends on Llama 3.1 8B capabilities
- Security scanning uses pattern recognition, not static analysis tools
- Generated tests need human review before use
This does work well for quick development feedback though.

## License

Do whatever you want with this code.