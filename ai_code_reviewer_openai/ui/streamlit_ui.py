import streamlit as st
from typing import Callable
from models.response_models import CodeReviewModel

class StreamlitUI:
    @staticmethod
    def initialize_app() -> None:
        st.set_page_config(page_title="An AI Code Reviewer", page_icon="💬", layout="centered")

        if "api_key_valid" not in st.session_state:
            st.session_state.api_key_valid = False
        if "api_key" not in st.session_state:
            st.session_state.api_key = ""
    
    @staticmethod
    def is_authenticated() -> bool:
        return st.session_state.api_key_valid
    
    @staticmethod
    def get_api_key() -> str:
        return st.session_state.api_key
    
    @staticmethod
    def set_authenticated_state(api_key:str, is_valid:bool) -> None:
        st.session_state.api_key = api_key
        st.session_state.api_key_valid = is_valid

    @staticmethod
    def display_error(message:str) -> None:
        st.error(message)

    @staticmethod
    def render_auth_page(on_verify_callback: Callable[[str], bool]) -> None:
        st.markdown("# 🔑 Enter OpenAI API Key")
        st.write("Please provide a valid OpenAI key to access the code review workspace.")

        input_key = st.text_input("OpenAI key", type="password", placeholder="sktiwx_se...")

        if st.button("Verify & Proceed"):
            if not input_key.strip():
                st.warning("API key cannot be empty")
            else:
                 with st.spinner("Authenticating client..."):
                     is_valid = on_verify_callback(input_key)
                     if is_valid:
                         st.success("API key authenticated successfully!")
                         st.rerun()
    
    @staticmethod
    def render_main_dashboard(on_logout_callback: Callable[[], None], on_submit_code: Callable[[str], None]) -> None:
        if st.button("Logout / Change key"):
            on_logout_callback()
            st.rerun()

        st.markdown("# 💬 An AI Code Reviewer")

        user_code = st.text_area(
            label="Enter your python code here...",
            placeholder= "import NUMPY as np\n\nprnt(np.random.randint(1, 10))",
            height=200
        )

        if st.button("Generate", type="secondary"):
            if not user_code.strip():
                st.warning("Input area is empty. Please feed valid script blocks.")
            else:
                with st.spinner("Analyzing semantics & execution trees..."):
                    on_submit_code(user_code)

    
    @staticmethod
    def render_review_results(result: CodeReviewModel) -> None:
        st.markdown("---")
        st.markdown("# Code Review")

        if result.has_bugs:
            st.markdown("## Bug Report")
            if result.bug_report:
                for bug in result.bug_report:
                    clean_bug = bug.lstrip("- ").strip()
                    st.markdown(f"- {clean_bug}")
            
            st.markdown("## Fixed code")
            if result.fixed_code:
                st.code(result.fixed_code, language="python")

        else:
            st.markdown("## ✅ Code Verification Passed")
            if result.code_review_report:
                for praise_point in result.code_review_report:
                    clean_point = praise_point.lstrip("- ").strip()
                    st.markdown(f"- {clean_point}")
                