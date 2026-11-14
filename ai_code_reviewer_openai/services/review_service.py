from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
from config.settings import AppSettings
from models.response_models import CodeReviewModel

class LangChainOpenAIReviewer:
    def __init__(self, api_key: str):
        self.config = AppSettings.load_from_yaml()
        self.api_key = api_key

    @staticmethod
    def validate_api_key(api_key:str) -> bool:
        try:
            client = OpenAI(api_key=api_key)
            client.models.list()
            return True
        except Exception:
            raise Exception("The provided API Key is invalid, expired, or unauthorized.")
        
    def analyze_code(self, code: str) -> CodeReviewModel:
        llm = ChatOpenAI(
            model=self.config.MODEL_NAME,
            api_key=self.api_key,
            temperature=0.1
        ).with_structured_output(CodeReviewModel, method="json_mode")

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "{System_Instructions}\n\nReturn your response as a valid json object matching the schema."),
            ("user","Please review the following python code:\n\n{user_code}")
        ])

        code_review_chain = prompt_template | llm

        return code_review_chain.invoke({
            "System_Instructions":self.config.SYSTEM_INSTRUCTION,
            "user_code": code
        })