from ui.streamlit_ui import StreamlitUI
from controller import SubtitleSearchEngineController

StreamlitUI.initialize_app()

if not StreamlitUI.is_authenticated():
    StreamlitUI.render_auth_page(SubtitleSearchEngineController.verify_openai_api_key)
elif SubtitleSearchEngineController.verify_vector_storage():
    StreamlitUI.render_main_dashboard(SubtitleSearchEngineController.handle_logout, SubtitleSearchEngineController.find_subtitles)

