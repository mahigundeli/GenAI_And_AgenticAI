from ui.streamlit_ui import StreamlitUI
from services.review_service import LangChainOpenAIReviewer

class CodeReviewController:
    @staticmethod
    def verify_api_key(api_key:str) -> bool:
        try:
            LangChainOpenAIReviewer.validate_api_key(api_key=api_key)
            StreamlitUI.set_authenticated_state(api_key=api_key, is_valid=True)
            return StreamlitUI.is_authenticated()
        except Exception as e:
            StreamlitUI.display_error(f"Authentication failed. Verify your credentials.\n\nDetails: {e}")
            return False
        
    @staticmethod
    def handle_logout() -> None:
        StreamlitUI.set_authenticated_state(api_key="", is_valid=False)

    @staticmethod
    def handle_code_submission(code: str) -> None:
        try:
            active_api_key = StreamlitUI.get_api_key()
            reviewer_service = LangChainOpenAIReviewer(api_key=active_api_key)
            analysis_result = reviewer_service.analyze_code(code=code)

            StreamlitUI.render_review_results(analysis_result)
        except Exception as e:
            StreamlitUI.display_error(f"An unexpected exception halted processing: {e}")
