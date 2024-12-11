from pdf2image import convert_from_path
import base64



def pdf2image(pdf_path:str ='./entrance-exams/ime.pdf'):
    """Convert a pdf to a list of images"""
    name = pdf_path.split('/')[-1].split('.')[0]
    pages = convert_from_path(pdf_path)

    # Save each page as a JPEG file using Pillow

    for i, page in enumerate(pages):
        page.save(f'./images/{name}_page_{i}.png', 'PNG')
        print(page)
    return convert_from_path(pdf_path)

def load_image(path) -> dict:
    """Load image from file and encode it as base64."""  
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    image_base64 = encode_image(path)
    
    return image_base64

if __name__ == "__main__":
    pages = convert_from_path('./entrance-exams/ime.pdf')
    for i, page in enumerate(pages):
        print(base64.b64encode(page.tobytes()).decode('utf-8'))
