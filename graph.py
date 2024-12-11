from parsers import (
    Page2TextState,
    OverallState,
    Window2QuestionsState,
)
import os
from pdf2image import convert_from_path
import base64
import json
from langgraph.graph import END, StateGraph, START
from langgraph.constants import Send
from agents import ocr_agent, initialize_question_parser_agent
from dotenv import load_dotenv
import argparse
load_dotenv()


def pages2image(state: OverallState):
    print('#'*10, state['pdf'], '#'*10)
    pdf_path = f'./entrance-exams/{state["pdf"]}'
    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        page.save(f'./page_{i}.png', 'PNG')
    pages = [f'./page_{i}.png' for i in range(len(pages))]
    pages_b64 = [ base64.b64encode(open(page, 'rb').read()).decode('utf-8') for page in pages]
    for page in pages:
        os.remove(page)
    # pages = [base64.b64encode(page.tobytes()).decode('utf-8') for page in pages]
    print(f'number of pages: {len(pages)}')
    if state['range_pages'][0]:
        return {'pages': pages_b64[state['range_pages'][0]:state['range_pages'][1]+1]}
    return {'pages': pages_b64}

def continue_to_ocr(state: OverallState):
    print('ocr pages')
    return [Send("image2text", {'base64_image':page,'index':i}) for i,page in enumerate(state['pages'])]

def image2text(state: Page2TextState):
    text = ocr_agent(state['base64_image'])
    return {"pages_text":[(state['index'],text)]}

def intermidiate(state: OverallState):
    print('parsing questions')
    return { }

def continue_to_parser(state: OverallState):
    pages = sorted(state['pages_text'], key=lambda x: x[0])
    sliding_pages = [pages[i][1] + '\n' + pages[i + 1][1] for i in range(len(pages) - 1)]
    return [Send("parse_questions", {'window_text': combined_page,'window_index':i}) for i,combined_page in enumerate(sliding_pages)]

def parse_questions(state: Window2QuestionsState):
    
    questions = initialize_question_parser_agent().invoke({
        "text": state['window_text']
    })
    return {"questions": [(state['window_index'],questions.questions)]}

def remove_duplicates(state: OverallState):
    final_questions = {}
    lists = [question_list[1] for question_list in sorted(state['questions'], key=lambda x: x[0])]
    for question_list in lists:
        for question in question_list:
            final_questions[question.index] =  question
    final_questions = [final_questions[i] for i in final_questions]
    print(f'number of questions found: {len(final_questions)}')
    return {"final_questions":final_questions}

def export_json(state: OverallState):
    print('exporting json')
    name = state['pdf'].split('.')[0]
    dump_data = [q.model_dump() for q in state['final_questions']]
    with open(f'./output_questions/{name}.json', 'w') as f:
        json.dump(dump_data, f,indent=4)
    return {}

def initialize_graph():
    graph = StateGraph(OverallState)

    graph.add_node("pages2image", pages2image)
    graph.add_node("image2text", image2text)
    graph.add_node("parse_questions", parse_questions)
    graph.add_node("intermidiate", intermidiate)
    graph.add_node("remove_duplicates", remove_duplicates)
    graph.add_node("export_json", export_json)

    graph.add_edge(START, "pages2image")
    graph.add_conditional_edges("pages2image", continue_to_ocr, ["image2text"])
    graph.add_edge("image2text", "intermidiate")
    graph.add_conditional_edges("intermidiate", continue_to_parser, ["parse_questions"])
    graph.add_edge("parse_questions", 'remove_duplicates')
    graph.add_edge('remove_duplicates', 'export_json')
    graph.add_edge('export_json', END)

    return graph.compile()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a PDF file.')
    parser.add_argument('--pdf', type=str, help='The name of the PDF file to process')
    parser.add_argument('--pages', type=str,default="", help='The range of pages to process, separated by a colon (e.g., "1:5")')

    args = parser.parse_args()
    if args.pages:
        try:
            start,end = (int(i) for i in args.pages.split(':'))
        except ValueError:
            print('Invalid range')
            exit(1)
    else:
        start,end = None,None
    state = {
        "pdf": args.pdf,
        "range_pages": (start,end)
    }

    graph = initialize_graph()
    graph.invoke(state)
    
