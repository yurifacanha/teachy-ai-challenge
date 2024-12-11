from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage
from prompts import (
    OCR_PAGE,
    PARSE_QUESTION
)
from parsers import Questions

def ocr_agent(image_64)-> str:
    model = ChatOpenAI(model="gpt-4o",temperature=0)
    r = model.invoke(
        [HumanMessage(
        content=[
        {"type": "text", "text": OCR_PAGE},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_64}"}},
        ])]
        )
    return r.content

def initialize_question_parser_agent() -> LLMChain:
    prompt_question = PromptTemplate(
        template=PARSE_QUESTION,
        input_variables=["text"],
    )
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    chain_question = prompt_question | model.with_structured_output(Questions)
    return chain_question


