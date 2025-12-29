import streamlit as st
from utils.code_analyzer import CodeReviewer
import os

# Page config
st.set_page_config(
    page_title="AI Code Review Assistant",
    layout="wide"
)

# Title
st.title(" AI Code Review Assistant")
st.markdown("**Powered by Groq AI** | Get instant code reviews, security analysis, and improvement suggestions")
# Sidebar
st.sidebar.title(" Settings")

# API Key input (optional - can use hardcoded one)
api_key = st.sidebar.text_input(
    "OpenAI API Key (Optional)",
    type="password",
    help="Get free $5 credits at platform.openai.com. Leave empty to use default."
)

if not api_key:
    api_key = os.getenv('OPENAI_API_KEY')

language = st.sidebar.selectbox(
    "Programming Language",
    ["python", "javascript", "java", "cpp", "go", "rust", "typescript"]
)

review_type = st.sidebar.multiselect(
    "Analysis Type",
    ["Code Quality", "Security Check", "Test Generation", "Performance"],
    default=["Code Quality", "Security Check"]
)

# Main input
st.markdown("###  Paste Your Code")

code_input = st.text_area(
    "Code to Review",
    height=300,
    placeholder=f"Paste your {language} code here..."
)

# Example codes
with st.expander(" Try Example Code"):
    example = st.selectbox(
        "Select Example",
        [
            "Vulnerable Login Function",
            "Inefficient Loop",
            "SQL Injection Risk",
            "Memory Leak",
            "Syntax Error - Missing Parentheses"
        ]
    )
    
    examples = {
        "Vulnerable Login Function": """def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    return cursor.fetchone()""",
        
        "Inefficient Loop": """def process_data(items):
    result = []
    for i in range(len(items)):
        for j in range(len(items)):
            if items[i] > items[j]:
                result.append(items[i])
    return result""",
        
        "SQL Injection Risk": """def get_user(user_id):
    query = "SELECT * FROM users WHERE id=" + user_id
    return db.execute(query)""",
        
        "Memory Leak": """class DataProcessor:
    cache = []
    
    def process(self, data):
        self.cache.append(data)
        return len(self.cache)""",
        
        "Syntax Error - Missing Parentheses": """def greeting:
    return "Hello, World!" """
    }
    
    if st.button("Load Example"):
        code_input = examples[example]
        st.rerun()

# Analyze button
col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    analyze_btn = st.button(" Analyze Code", type="primary", use_container_width=True)

with col2:
    clear_btn = st.button(" Clear", use_container_width=True)

if clear_btn:
    st.rerun()

# Analysis
if analyze_btn:
    if not code_input.strip():
        st.error("Please paste code to analyze!")
    else:
        try:
            reviewer = CodeReviewer(api_key=api_key)
            
            # Code Quality Review
            if "Code Quality" in review_type:
                with st.spinner("Analyzing code quality..."):
                    quality_review = reviewer.analyze_code(code_input, language)
                
                st.markdown("---")
                st.markdown("##  Code Quality Review")
                st.markdown(quality_review)
            
            # Security Check
            if "Security Check" in review_type:
                with st.spinner("Checking security vulnerabilities..."):
                    security_review = reviewer.check_security(code_input, language)
                
                st.markdown("---")
                st.markdown("##  Security Analysis")
                st.markdown(security_review)
            
            # Test Generation
            if "Test Generation" in review_type:
                with st.spinner("Generating test cases..."):
                    tests = reviewer.suggest_tests(code_input, language)
                
                st.markdown("---")
                st.markdown("##  Suggested Tests")
                st.markdown(tests)
            
            # Performance
            if "Performance" in review_type:
                st.markdown("---")
                st.markdown("## ⚡ Performance Analysis")
                st.info("Performance analysis included in Code Quality section.")
            
        except ValueError as e:
            st.error(f"Configuration Error: {str(e)}")
            st.info(" Tip: Make sure you've added your OpenAI API key in the code or sidebar.")
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

# Features section
st.markdown("---")
st.markdown("###  Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ** Code Quality**
    - Syntax error detection
    - Style & formatting issues
    - Best practices violations
    - Complexity analysis
    - Refactoring suggestions
    """)

with col2:
    st.markdown("""
    ** Security**
    - Vulnerability detection
    - SQL injection checks
    - XSS prevention
    - Authentication issues
    - Input validation
    """)

with col3:
    st.markdown("""
    ** Testing**
    - Auto-generate test cases
    - Edge case identification
    - Mock data examples
    - Coverage suggestions
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray;">
    <p>Built with OpenAI GPT-4 | Not a replacement for human code review</p>
    <p>Always verify suggestions before applying to production code</p>
</div>
""", unsafe_allow_html=True)