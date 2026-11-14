from ui.streamlit_ui import StreamlitUI
from controller import CodeReviewController
 
StreamlitUI.initialize_app()

if not StreamlitUI.is_authenticated():
    StreamlitUI.render_auth_page(
        on_verify_callback=CodeReviewController.verify_api_key
    )
else:
    StreamlitUI.render_main_dashboard(
        on_logout_callback=CodeReviewController.handle_logout,
        on_submit_code=CodeReviewController.handle_code_submission
    )