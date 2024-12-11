import cv2
import numpy as np
from ultralytics import YOLO
import uuid
import base64
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os 
import glob

result_folder = "./image_extractor/inferences/detected/"
new_image_folder = "./image_extractor/inferences/images/"
images_folder = "./image_extractor/images/"
model = YOLO("./image_extractor/model.pt")  # pretrained YOLOv8n model
font_path = "./image_extractor/font.ttf"

def iou(box1, box2):
    """Compute the Intersection over Union (IoU) of two bounding boxes."""
    x1, y1, x2, y2 = box1
    x1_b, y1_b, x2_b, y2_b = box2

    xi1 = max(x1, x1_b)
    yi1 = max(y1, y1_b)
    xi2 = min(x2, x2_b)
    yi2 = min(y2, y2_b)

    inter_area = max(xi2 - xi1, 0) * max(yi2 - yi1, 0)

    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_b - x2_b) * (y2_b - y1_b)

    union_area = box1_area + box2_area - inter_area

    iou = inter_area / union_area
    return iou


def merge_boxes(boxes, threshold=0.5):
    """Merge bounding boxes based on IoU."""
    if len(boxes) == 0:
        return []

    boxes = sorted(boxes, key=lambda x: x[1])
    retry = True

    while retry:
        retry = False
        for i in range(len(boxes)):
            base_box = boxes[i]
            for idx, box in enumerate(boxes):
                if idx == i:
                    continue
                t = iou(base_box, box)
                if t > threshold:
                    retry = True
                    merged_box = [
                        min(base_box[0], box[0]),
                        min(base_box[1], box[1]),
                        max(base_box[2], box[2]),
                        max(base_box[3], box[3]),
                    ]
                    del boxes[idx]
                    del boxes[i]
                    boxes.append(merged_box)
                    break
            if retry:
                break

    return boxes


def random_name(extension):
    return str(uuid.uuid4()) + ".%s" % (extension,)


def convert_image_to_base64(image):
    _, buffer = cv2.imencode(".jpg", image)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text.decode("utf-8")


def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 200, 1)):
        text_size = cv2.getTextSize(text, cv2.QT_FONT_NORMAL, scale / 10, 1)[0]
        if text_size[0] <= width:
            return scale / 10
    return 1


def create_blank_image(h, w, object_name):

    def find_max_font_size(text, image_width, image_height, font_path):
        font_size = image_height
        font = ImageFont.truetype(font_path, font_size)
        text_width = draw.textlength(text, font=font)

        while text_width > image_width:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)
            text_width = draw.textlength(text, font=font)

        return font_size

    
    color = (0, 0, 0)  

    blank_square = np.ones((h, w, 3), dtype=np.uint8) * 255
    image_pil = Image.fromarray(blank_square)  
    draw = ImageDraw.Draw(image_pil)

    max_font_size = max(find_max_font_size(object_name, w, h, font_path), 10)
    font = ImageFont.truetype(font_path, max_font_size)

    text_width = draw.textlength(object_name, font=font)

    position = ((w - text_width) // 2, (h - max_font_size) // 2)

    draw.text(position, object_name, font=font, fill=color)
    image_with_text = np.array(image_pil)  # Convert PIL image back to OpenCV image

    return image_with_text


def replace_images(img_name):
    x = images_folder+img_name
    img = cv2.imread(x)


    results = model([img], conf=0.45, iou=0.6)  
    for i, result in enumerate(results):
        boxes = result.boxes.xyxy  
        boxes = merge_boxes(boxes, threshold=0.05) 

        for j, box in enumerate(boxes):
            object_name = f'<img>{j}</img>'

            x1, y1, x2, y2 = map(int, box)  # Convert box coordinates to integers
            width, height = x2 - x1, y2 - y1

            
            blank_square = create_blank_image(height, width, object_name)

            contiguous_img = np.ascontiguousarray(img[y1:y2, x1:x2])
            detected_name = f'{result_folder}{j}_{img_name}'
            cv2.imwrite(detected_name, contiguous_img)
            print("Detected object saved as", detected_name)
            
            # Replace the detected object in the original image with the blank square
            img[y1:y2, x1:x2] = blank_square
        
        
        #save the new image
        cv2.imwrite(new_image_folder+img_name, img)


        return 


if __name__ == "__main__":
    # Get a list of all images in the images folder
    image_files = glob.glob(images_folder + "*.png")

    # Process each image
    for image_file in image_files:
        img_name = os.path.basename(image_file)
        replace_images(img_name)







