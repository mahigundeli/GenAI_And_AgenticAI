from typing import List, Optional
from pydantic import BaseModel, Field

class Subtitle_Match_Result(BaseModel):
    match_found: bool = Field(
        description="True if one of the database documents clearly matches the input subtitle text. False if none fit."
    )
    subtitle_number: Optional[str] = Field(
        None,
        description="The exact 'subtitle_number' extracted from the matching document metadata. Return None if match_found is False."
    )
    subtitle_name: Optional[str] = Field(
        None,
        description="The exact 'subtitle_name' extracted from the matching document metadata. Return None if match_found is False."
    )
    confidence_reasoning: str = Field(
        description="A short, clear sentence explaining what occurs in this scene and why it matches the user's text."
    )
    exact_matching_quote: Optional[str] = Field(
        None,
        description="A short snippet from the text document that directly corresponds to the query context."
    )