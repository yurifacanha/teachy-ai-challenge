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


if __name__ == "__main__":


    text = """

        LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS  
        Questões de 01 a 45  
        Questões de 01 a 05 (opção inglês)  

        QUESTÃO 01  

        No man is an island,  
        Entire of itself;  
        Every man is a piece of the continent,  
        A part of the main.  
        [...]  
        Any man’s death diminishes me,  
        Because I am involved in mankind.  

        DONNE, J. The Works of John Donne. Londres: John W. Parker, 1839 (fragmento).  

        Nesse poema, a expressão “No man is an island” ressalta o(a)  
        A medo da morte.  
        B ideia de conexão.  
        C conceito de solidão.  
        D risco de devastação.  
        E necessidade de empatia.  

        QUESTÃO 02  

        Things We Carry on the Sea  

        We carry tears in our eyes: good-bye father, good-bye mother  
        We carry soil in small bags: may home never fade in our hearts  
        We carry carnage of mining, droughts, floods, genocides  
        We carry dust of our families and neighbors incinerated in mushroom clouds  
        We carry our islands sinking under the sea  
        We carry our hands, feet, bones, hearts and best minds for a new life  
        We carry diplomas: medicine, engineer, nurse, education, math, poetry, even if they mean nothing to the other shore  
        We carry railroads, plantations, laundromats, bodegas, taco trucks, farms, factories, nursing homes, hospitals, schools, temples... built on our ancestors’ backs  
        We carry old homes along the spine, new dreams in our chests  
        We carry yesterday, today and tomorrow  
        We’re orphans of the wars forced upon us  
        We’re refugees of the sea rising from industrial wastes  
        And we carry our mother tongues  
        [...]  
        As we drift... in our rubber boats... from shore... to shore... to shore...  

        PING, W. Disponível em: https://poets.org. Acesso em: 1 jun. 2023.  

        Ao retratar a trajetória de refugiados, o poema recorre à imagem de viagem marítima para destacar o(a)  
        A risco de choques culturais.  
        B impacto do ensino de história.  
        C importância da luta ambiental.  
        D existência de experiências plurais.  
        E necessidade de capacitação profissional.  

        QUESTÃO 03  

        The average american tosses 300 pounds of food each year, making food the number one contributor to America’s landfills. Eat your leftovers and keep your perishables in the fridge – the Earth is counting on it.  

        Disponível em: https://mir-s3-cdn-cf.behance.net. Acesso em: 29 out. 2021 (adaptado).  

        Esse cartaz de campanha sugere que  
        A os lixões precisam de ampliação.  
        B o desperdício degrada o ambiente.  
        C os mercados doam alimentos perecíveis.  
        D a desnutrição compromete o raciocínio.  
        E as residências carecem de refrigeradores. 
        """

    chain_question = initialize_question_parser_agent()
    q = chain_question.invoke({
        "text": text
    })
