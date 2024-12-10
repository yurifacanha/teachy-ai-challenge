# Teachy AI Challenge

## General Instructions

1. Fork this repository and develop what is asked bellow.
2. Let us know when you are done.

## The Challenge


You'll create a Proof of Concept of a pipeline that extracts questions from entrance exams PDFs.

There are two types of questions. You should consider:
- Multiple Choice Questions:
    - These questions are composed of two elements:
      - Statement
      - Alternatives
- Open Ended Questions:
    - These questions are composed of one elements:
      - Statement

PoC's Specifications:

### MUST HAVEs:
- Accept PDF inputs
- Extract the aforementioned components of each type of question
- Extract Support Text for questions
- Extract images and link them to their question(s)
- Support exams that have a two-column layout
- Enumerate Questions correctly
- Question carry over from one page to the next

### NICE TO HAVEs:
- Represent Equations correctly in LaTeX
- Represent Chemical Formulas correctly

Example JSON of a question should look like this:

```json
{
  "question_number": "3",
  "question_type": "MultipleChoice",
  "statement": "...",
  "Alternatives": ["...", "...", "...", "..."],
  "image": "link to image, if there's an image associated with the question",
  "suport_text": "Suport Text if there's a support text associeated with the question"
}
```

## What You Should Deliver:

You'll receive 10 entrance exams PDFs. Your output should be:
1. The code that you wrote for extracting questions out of these PDFs
2. Your reasoning explanaied in the readme
3. 10 folders, one for each exam, each one with JSONs of questions for that exam

Feel free to reach out for any questions that you may have about the challenge!

Best of Luck!
