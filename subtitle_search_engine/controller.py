import os
from ui.streamlit_ui import StreamlitUI
from config.settings import AppSettings
from services.subtitle_db_service import Subtitles_DB_Service
from services.vector_storage_service import Vector_Storage_Service
from services.subtitle_analyzer_service import LangchainOpenAISubtitleAnalyzer

class SubtitleSearchEngineController:

    @staticmethod
    def verify_openai_api_key(api_key:str) -> bool:
        try:
            if LangchainOpenAISubtitleAnalyzer.validate_api_key(api_key=api_key):
                StreamlitUI.set_authenticated_state(api_key=api_key, is_valid=True)
                return StreamlitUI.is_authenticated()
        except Exception as e:
            StreamlitUI.display_error(f"Authentication failed. Verify your credentials.\n\nDetails: {e}")
            return False
        
    @staticmethod
    def handle_logout() -> None:
        StreamlitUI.set_authenticated_state(api_key="", is_valid=False)

    @staticmethod
    def verify_vector_storage() -> bool:
        api_key = StreamlitUI.get_api_key()
        vector_storage = Vector_Storage_Service()
        if vector_storage.load_existing_vector_store(api_key=api_key):
            return True
        
        StreamlitUI.ask_user_to_build_vector_storage(api_key, SubtitleSearchEngineController.build_vector_storage)
        return False
        
    @staticmethod
    def build_vector_storage(api_key: str) -> None:
        api_key = StreamlitUI.get_api_key()
        app_settings = AppSettings.load_from_yaml()
        file_relative_path = app_settings.DB_FILE_RELATIVE_PATH
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_file_path = os.path.join(current_dir, file_relative_path)

        print(f"DB FILE PATH: {db_file_path}")

        db_handler = Subtitles_DB_Service(db_file_path)
        subtitles_contents = db_handler.get_cleaned_subtitles(startRow=1,endRow=20000)
        print(f"Subtitles contents count: {len(subtitles_contents)}")

        vector_storage = Vector_Storage_Service()
        vector_storage.prepare_documents(subtitles_contents)
        print("Prepared documents...")
        vector_storage.build_vector_store(api_key=api_key)
        StreamlitUI.rerun()

    @staticmethod
    def find_subtitles(api_key: str, subtitle_text: str) -> None:
        vector_storage = Vector_Storage_Service()
        vector_storage.load_existing_vector_store(api_key=api_key)
        similarity_results = vector_storage.get_similarity_search_results(api_key=api_key,query_subtitle=subtitle_text)

        subtitle_analyzer = LangchainOpenAISubtitleAnalyzer(api_key=api_key)
        subtitle_match_result = subtitle_analyzer.find_subtitle(subtitle_text=subtitle_text, similarity_results=similarity_results)
        
        StreamlitUI.render_subtitle_result(subtitle_match_result)