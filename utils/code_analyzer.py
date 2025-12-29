import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class CodeReviewer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required")
        
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize Groq client: {str(e)}")
    
    def analyze_code(self, code, language="python"):
        if not code or not code.strip():
            raise ValueError("Code cannot be empty")
        
        if len(code) > 10000:
            raise ValueError("Code exceeds maximum length of 10000 characters")
        
        prompt = f"""You are an expert code reviewer. Analyze this {language} code and provide a comprehensive review:

```{language}
{code}
```

Provide:

## Score: X/100

Rate based on: correctness, readability, efficiency, and best practices.

## Issues Found

List only the MOST IMPORTANT issues (maximum 5). For each:
- Severity (CRITICAL/HIGH/MEDIUM)
- What's wrong
- Why it matters

## Key Improvements

Provide 2-3 actionable improvements with code examples.

## Refactored Code
```{language}
[improved version]
```

Keep it concise and practical. Focus on what matters most.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer who provides detailed, actionable feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            if not response.choices or len(response.choices) == 0:
                raise Exception("Empty response from API")
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    def check_security(self, code, language="python"):
        if not code or not code.strip():
            raise ValueError("Code cannot be empty")
        
        if len(code) > 10000:
            raise ValueError("Code exceeds maximum length of 10000 characters")
        
        prompt = f"""You are a security expert analyzing {language} code for vulnerabilities.

Analyze this code for security issues:

```{language}
{code}
```

Rules:
- Only report vulnerabilities that are ACTUALLY PRESENT in this specific code
- If the code doesn't interact with databases, don't mention SQL injection
- If the code doesn't handle web input, don't mention XSS
- If the code doesn't use authentication, don't mention auth issues
- Be specific and practical

If the code is a simple algorithm or utility function with no security concerns, say:
"No significant security vulnerabilities detected. This appears to be a simple utility function."

Otherwise, for each REAL vulnerability found:

## [Vulnerability Name]

**Severity:** CRITICAL/HIGH/MEDIUM/LOW
**Location:** Specific line or section
**Issue:** What's actually wrong
**Fix:** How to fix it with code example
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a security expert who identifies vulnerabilities in code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            if not response.choices or len(response.choices) == 0:
                raise Exception("Empty response from API")
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Security check failed: {str(e)}")
    
    def suggest_tests(self, code, language="python"):
        if not code or not code.strip():
            raise ValueError("Code cannot be empty")
        
        if len(code) > 10000:
            raise ValueError("Code exceeds maximum length of 10000 characters")
        
        prompt = f"""You are a testing expert. Generate comprehensive test cases for this {language} code:

```{language}
{code}
```

Generate tests covering:

1. Normal Cases: Expected behavior with valid inputs
2. Edge Cases: Boundary conditions, empty inputs, large inputs
3. Error Cases: Invalid inputs, exceptions, error handling

Provide complete, runnable test code using the appropriate testing framework:
- Python: pytest
- JavaScript/TypeScript: Jest
- Java: JUnit

Format:

## Test Suite Overview

Brief description of testing strategy and coverage.

## Test Code

```{language}
[complete test code that can be run as-is]
```

## Test Cases Explained

List each test case with what it tests, expected outcome, and why it matters.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a testing expert who writes comprehensive test suites."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            if not response.choices or len(response.choices) == 0:
                raise Exception("Empty response from API")
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Test generation failed: {str(e)}")