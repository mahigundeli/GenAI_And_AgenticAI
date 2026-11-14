import streamlit as st
from typing import Callable
from models.subtitle_match_result import Subtitle_Match_Result

class StreamlitUI:

    @staticmethod
    def initialize_app() -> None:
        st.set_page_config(page_title="Subtitle Search Engine", page_icon="💬", layout="centered")

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
    def set_authenticated_state(api_key: str, is_valid: bool) -> None:
        st.session_state.api_key = api_key
        st.session_state.api_key_valid = is_valid

    @staticmethod
    def display_error(message: str) -> None:
        st.error(message)

    @staticmethod
    def rerun() -> None:
        st.rerun()

    @staticmethod
    def render_auth_page(on_verify_callback: Callable[[str], bool]) -> None:
        st.markdown("# 🔑 Enter OpenAI API Key")
        st.write("Please provide a valid OpenAI key to access the code review workspace.")

        input_key = st.text_input("OpenAI key", type="password", placeholder="seticuekc..")

        if st.button("Verify & Proceed"):
            if not input_key.strip():
                st.warning("API key cannot be empty")
            else:
                with st.spinner("Authenticating client..."):
                    is_valid = on_verify_callback(input_key)
                    if is_valid:
                        st.success("API eky authenticated successfully!")
                        st.rerun()

    @staticmethod
    def ask_user_to_build_vector_storage(api_key: str, build_vector_storage_callback: Callable[[str], None]) -> None:
        st.markdown("# Subtitle storage is empty")
        st.write("Subtitle storage is not built. Do you want to build subtitle storage?")

        if st.button("Yes",type="secondary"):
            with st.spinner("Building vector storage..."):
                build_vector_storage_callback(api_key)

    @staticmethod
    def render_main_dashboard(on_logout_callback: Callable[[str], None], on_find_subtitle: Callable[[str], None]) -> None:
        if st.button("Logout / Change key"):
            on_logout_callback()
            st.rerun()

        st.markdown("# 💬 Subtitle Search Engine")

        subtitle_text = st.text_area(
            label= "Enter some part of movie/series subtitle here...",
            placeholder="If you want to experience what it is to be fathered by god... Your perfect father in heaven can change the trajectory of your life. Your daddy wants to restore you. There is a loving father in heaven who has created us. And he wants a relationship with us. I got a full scholarship to go to Miami university in Oxford, Ohio.",
            height=200
        )

        if st.button("Find Subtitle", type="secondary"):
            if not subtitle_text.strip():
                st.warning("Input area in empty. Please feed some part of subtitle")
            else:
                with st.spinner("Analyzing subtitle & finding movie/series subtitle url..."):
                    api_key = StreamlitUI.get_api_key()
                    on_find_subtitle(api_key, subtitle_text.strip())

    @staticmethod
    def render_subtitle_result(result: Subtitle_Match_Result) -> None:
        st.markdown("---")
        st.markdown("# Subtitle result")

        if result.match_found and result.subtitle_name.strip():
            st.markdown(f"##### Movie/Series subtitle file name: {result.subtitle_name.strip()}")
            st.write(f"Subtitle url:  https://www.opensubtitles.org/en/subtitles/{result.subtitle_number}")
        else:
            st.write("No matching movie/series found for provided subtitle")
        
        