
## Usage
first create a virtual enviroment and install dependecies
```bash
pip install -r requirements.txt
```
Then set your openai api KEY (.env file):
```
OPENAI_API_KEY = 'your key'
```

To process a PDF file and analyze specific pages, use the following command:

```bash
python graph.py --pdf <filename.pdf> --pages <start:end>
```
##### Example

To process pages 5 through 8 of a PDF file named name.pdf, run:
```
python graph.py --pdf name.pdf --pages 5:8
```

The result will be saved as a JSON file in the `output_folder`, with the same name as the input PDF but with a `.json` extension.
Example:
```json
[
    {
        "index": 21,
        "statement": "Inicialmente, um poste, fabricado com material de coeficiente de dilatação volumétrica \\(\\gamma\\), tem as dimensões indicadas na figura, estando o ponto A fixo. Ao ser submetido a um aumento de temperatura \\( T \\), o ponto B é deslocado de:",
        "options": [
            {
                "order": "A",
                "value": "\\frac{\\sqrt{17}\\gamma TL}{4}"
            },
            {
                "order": "B",
                "value": "\\frac{5\\gamma TL}{12}"
            },
            {
                "order": "C",
                "value": "\\frac{\\sqrt{17}\\gamma TL}{21}"
            },
            {
                "order": "D",
                "value": "\\frac{\\sqrt{17}\\gamma TL}{12}"
            },
            {
                "order": "E",
                "value": "\\frac{\\gamma TL}{4}"
            }
        ],
        "type": 0,
        "background_text": ""},
        ...
    ]
```
Where :
- **index**: number of the question
- **statement**: question statement.
- **options**: A list of alternatives or choices related to the statement (multiple choices).
- **type**: 0 for multiple choice , 1 for open ended
- **background_text**: support text for the question if exists 

## Solution Explanation

The solution is based on a **LangGraph pipeline approach** using the **MapReduce** paradigm to ensure efficient processing. Below is a detailed explanation of the steps:

1. **PDF to Images**: 
   - The PDF is divided into individual pages.
   - Each page is converted into an image.

2. **OCR Text Extraction**:
   - Text is extracted from each page image in parallel using OpenAI's OCR solution.
   - This OCR is capable of handling complex layouts, including multi-column text, ensuring high-quality text extraction.

3. **Sliding Window Approach**:
   - To handle overlapping questions between pages, we use sliding windows:
     - Example: Page 1-2, Page 2-3, ..., until the end.
   - This overlap helps capture questions split across page boundaries.

4. **Question Extraction**:
   - For each sliding window, questions are extracted using a structured format defined with **Pydantic**.
   - MapReduce parallelism ensures efficient processing for each window.

5. **Deduplication**:
   - After extracting the list of questions, duplicates are removed by keeping the **last occurrence** of each question.

6. **Export**:
   - The final list of unique questions is exported in the desired format.

### Visual Representation

The process is illustrated in the image below:

![Process Overview](path/to/your/image.png)

This structured approach ensures scalability, accuracy, and efficiency, leveraging parallelism and robust question extraction methods. Let me know if you want to refine or add further details!

### Important Notes

#### OCR Justification

While the current solution leverages OpenAI's OCR due to its ability to handle multi-column layouts and complex text structures, it may introduce latency issues. Traditional OCR solutions could be considered for better performance; however, they often struggle with specific use cases, such as parsing LaTeX formulas and equations in mathematical and chemical contexts.

**Proposed Alternative:**
- Use **PubLayNet** (a dataset for document layout analysis) or a custom **YOLO** model to detect and extract formulas and equations. These components can then be parsed individually for more accurate results.
- This hybrid approach could combine the strengths of both traditional OCR for general text and specialized models for structured content like formulas.

#### Image Linking and Extraction

Due to time constraints, the image extraction approach was not fully integrated into the pipeline. However, a solution exists in the `image_extractor` folder, which employs a YOLO-based model to detect and extract images from pages. 

**Process Summary:**
1. **Detection**:
   - Images are detected and cropped using YOLO.
   - Detected images are replaced with placeholders.
2. **OCR Integration**:
   - Placeholders are passed through the OCR process, ensuring the solution identifies which image is linked to each question.
3. **Challenges**:
   - The current solution uses geometric heuristics to avoid cropping necessary content during image detection.
   - Further adjustments are needed to improve accuracy and prevent OCR interference.

#### Example Output

Below is an example of the image extraction process and how placeholders relate to the original content:

##### Original 

![Source](/image_extractor/images/enem_page_8.png)

##### Placeholders

![Placeholders](/image_extractor/inferences/images/enem_page_8.png)

##### Cropped

![Cropped1](/image_extractor/inferences/detected/0_enem_page_8.png)
![Cropped1](/image_extractor/inferences/detected/1_enem_page_8.png)

