from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from models.subtitle_match_result import Subtitle_Match_Result
from config.settings import AppSettings

class LangchainOpenAISubtitleAnalyzer:
    def __init__(self, api_key: str):
        settings = AppSettings.load_from_yaml()
        self.llm = ChatOpenAI(
            model= settings.OPENAI_SUBTITLE_ANALYZER_MODEL,
            api_key= api_key,
            temperature=0,
        )
        
        self.structured_llm = self.llm.with_structured_output(Subtitle_Match_Result)

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a subtitle matching assistant.
             Your task is to compare the user's provided "Subtitle Text" against a list of labeled choices from a search engine database.
             
             Instructions:
             1. Carefully read the "Subtitle Text" provided by the user.
             2. Look at each labeled choice inside the "Choices Context" block (e.g., Choice #1, Choice #2).
             3. Determine if any of the choices are a direct semantic match for the user's text.
             4. Extract the correct 'subtitle_number' and 'subtitle_file_name' from the matching choice block.
             5. In the 'confidence_reasoning' field, write a short, clear, and objective description summarizing what occurs within that matching scene based strictly on the text provided in that choice. This must be a clean, natural sentence.
             6. In the 'exact_matching_quote' field, extract a short snippet from the matching document that directly corresponds to the query context.
             
             Choices Context:
             {context}
             
             User Subtitle Text to Match:
             {subtitle_text}"""),
            ("human", "{subtitle_text}")
        ])

    def find_subtitle(self, subtitle_text: str, similarity_results: list[tuple[Document, float]]) -> Subtitle_Match_Result:
        context_string = self.format_context(similarity_results)

        chain = self.prompt_template | self.structured_llm

        result: Subtitle_Match_Result = chain.invoke(
            {
                "context" : context_string,
                "subtitle_text": subtitle_text
            }
        )

        print(result)

        return result
    
    def format_context(self, similarity_results: list[tuple[Document, float]]) -> str:
        formatted_text = ""

        for i, (doc, score) in enumerate(similarity_results, start=1):

            sub_num = doc.metadata.get('subtitle_number', 'Unknown')
            sub_name = doc.metadata.get('subtitle_name', 'Unknown')

            formatted_text += f"-- Choice #{i} --\n"
            formatted_text += f"Subtitle number: {sub_num}\n"
            formatted_text += f"Subtitle file name: {sub_name}\n"
            formatted_text += f"Search relevance score: {score:.4f}\n"
            formatted_text += f"Subtitle text:\n{doc.page_content}"

        return formatted_text
    
    @staticmethod
    def validate_api_key(api_key:str) -> bool:
        try:
            client = OpenAI(api_key=api_key)
            client.models.list()
            return True
        except Exception:
            raise Exception("The provided API Key is invalid, expired, or unauthorized.")
        