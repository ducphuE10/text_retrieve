from PIL import Image
from pytesseract import pytesseract

#Define path to tessaract.exe
def extract_text_from_img(path_to_image):
    path_to_tesseract = "/usr/bin/tesseract"

    #Point tessaract_cmd to tessaract.exe
    pytesseract.tesseract_cmd = path_to_tesseract

    #Open image with PIL
    img = Image.open(path_to_image)

    #Extract text from image
    text = pytesseract.image_to_string(img)

    # print(text)
    with open("text.txt", "wa") as text_file:
        text_file.write(text)