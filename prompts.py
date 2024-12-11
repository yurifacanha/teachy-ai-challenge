OCR_PAGE = """The image is a test with questions. make the ocr of the image.
<rules>
keep attention in math formulas to convert them to latex 
for chemical formulas, use chemfig package when you need to represent them
put latex equations always into the folowing  delimiters \[...\] or $$...$$
Do NOT include triple backticks when generating text. should be plain text.
NEVER generate content that is not included in the image.
inside the image we have images. Do not generate content for the images inside the image.
</rules>
"""

PARSE_QUESTION = """ Given this page with many questions , you must provide for each question the following information:
0. Index: the question index in the document (Question number). Exemple: Questão 1, Questão 2, Questão 3 (indexes: 1,2,3)
1. the type:  multiple choice(0),open ended (1)
2. The statement: The statement is the core part of the question or problem. It defines what the user is expected to solve, calculate, or interpret. It typically includes the main task, key variables, and relevant data (e.g., mathematical matrices, equations, or a problem description), excluding the alternatives and support text
3. The alternatives: a list of alternatives with the order and text
4. Background Text: if there's a background text associeated with the question(ex: Poems,news,narrative texts, background texts for context). The entire text must be included in the background text field

<rules>
-alternatives are always must be empty if the question is open ended
-you cannot add or remove content for the question 
-all input data (like constants, formulas or tips to be used in the question) and observations must be included in the statement, not in the background text
- background text and alternatives cannot be in the statement
- different questions can have the same background text because sometimes the same text is used to contextualize different questions (repeat the background text for each question)
</rules>

Question: 

{text}

"""

