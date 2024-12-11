from typing import TypedDict
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List,Tuple
from typing import Annotated
import operator


# Initialize the AI model
model = ChatOpenAI(model="gpt-4o",temperature=0)



# Save each page as a JPEG file using Pillow


class Alternatives(BaseModel):
    """Multiple choices alternatives"""

    order: str = Field(description="option index(always a single letter)")
    value: str = Field(description="option text")

class Question(BaseModel):
    """Question formatted"""
    index : int = Field(description="question index. Always a number that indexes the question in the document")
    statement: str = Field(description="the hole question , excluding the alternatives")
    options: List[Alternatives] = Field(description="list of alternatives")
    type: int = Field(description="question type (0: multiple choice, 1: open ended)")
    background_text: str = Field(description="background text if there's any")

class Questions(BaseModel):
    questions : List[Question] = Field(description="list of questions")

class OverallState(TypedDict):
    """ Estado do formatador """
    pdf: str
    range_pages: tuple
    pages: List[str]
    final_questions : List[Question]
    pages_text: Annotated[List[tuple], operator.add]
    questions: Annotated[List[tuple], operator.add]

class Page2TextState(TypedDict):
    """ Image to text state """
    base64_image : str
    index : int

class Window2QuestionsState(TypedDict):
    """ Window to questions state """
    window_text: str
    window_index: int
