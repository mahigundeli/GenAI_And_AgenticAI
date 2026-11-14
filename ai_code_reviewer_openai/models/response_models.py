from pydantic import BaseModel, Field
from typing import List, Optional

class BugIssue(BaseModel):
    description: str = Field(description="A clear description of the bug or issue found.")
    location: str = Field(description="The function, class, or line where the issue occurs.")

class CodeReviewModel(BaseModel):
    has_bugs: bool = Field(
        ...,
        description="Set to True if the code contains bugs, syntax errors, or major performance flaws. Set to False if the code is excellent and needs no changes."        
    )
    bug_report: Optional[List[str]] = Field(
        default=None, 
        description="A list of separate bullet points describing the bugs found. Leave this empty/None if has_bugs is False."
    )
    fixed_code: Optional[str] = Field(
        default=None,
        description="The complete, corrected Python code block. Leave this empty/None if has_bugs is False."
    )
    code_review_report: Optional[List[str]] = Field(
        default=None,
        description="A bulleted list of praise analyzing the clean code architecture. Leave this empty/None if has_bugs is True."
    )