import io
import PyPDF2
import spacy
import json
from spacy.tokens import DocBin
from tqdm import tqdm
from spacy.util import filter_spans
import base64
from src.utils.create_and_split_data import (
    split_and_create_files,
    format_text,
    strip_accents,
)
from PIL import ImageEnhance, ImageFilter
import time
import pytesseract
from pdf2image import convert_from_bytes, convert_from_path
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
import os
from PIL import Image as PILImage
# os.environ['OMP_THREAD_LIMIT'] = '1'

import random
import easyocr
import numpy as np

# def preprocess_images_for_ocr(images, folder_name):
#     # Check if images is a single image or a list
#     base_path = os.path.join("images", str(folder_name))
#     images_to_process = [images] if not isinstance(images, list) else images
    
#     processed_images = []

#     for idx, pil_image in enumerate(images_to_process):
#         # image_folder = os.path.join(base_path, f"image_{idx+1}")
#         # os.makedirs(image_folder, exist_ok=True)

#         # Save the original image for later comparison
#         # original_path = os.path.join(image_folder, "original.jpg")
#         # pil_image.save(original_path)
#         # Convert the PIL Image to bytes
#         with io.BytesIO() as output:
#             pil_image.save(output, format='JPEG')
#             image_bytes = output.getvalue()

#         # Use Wand to preprocess the image bytes
#         with Image(blob=image_bytes) as img:
#             # Convert to grayscale
#             img.type = 'grayscale'

#             # Enhance contrast
#             img.contrast_stretch(0.02 * img.quantum_range, 0.98 * img.quantum_range)

#             # Binarize image
#             img.threshold(0.5)

#             # # Remove noise and smooth image
#             img.gaussian_blur(radius=1, sigma=0.5)

#             # Deskew image (auto-correct rotation)
#             # img.deskew(threshold=0.4)

#             # Resize image if needed, for example to DPI for OCR
#             # target_dpi = 500
#             # scaling_factor = target_dpi / (img.resolution[0])
#             # img.resize(int(img.width * scaling_factor), int(img.height * scaling_factor))

#             # Append the processed image to the list as a PIL Image
#             processed_images.append(PILImage.open(io.BytesIO(img.make_blob('JPEG'))))

#             # processed_path = os.path.join(image_folder, "processed.jpg")
#             # img.save(filename=processed_path)

#     # Return a list only if the original input was a list, otherwise return a single image
#     return processed_images if isinstance(images, list) else processed_images[0]

def melhorar_contraste_e_suavizar(images):
    new_images = []
    for image in images:
        img_gray = image.convert("L")
        # img_blurred = img_gray.filter(ImageFilter.GaussianBlur(radius=0.3))
        # enhancer = ImageEnhance.Contrast(img_blurred)
        # img_contrast = enhancer.enhance(2.0)
        new_images.append(img_gray)
    return new_images

# def melhorar_contraste_e_suavizar(images):
#     new_images = []
#     for image in images:
#         # Convert to grayscale
#         img_gray = image.convert('L')

#         # Apply a slight Gaussian blur (can be adjusted or omitted)
#         img_blurred = img_gray.filter(ImageFilter.GaussianBlur(radius=0.5))

#         # Enhance contrast
#         enhancer = ImageEnhance.Contrast(img_blurred)
#         img_contrast = enhancer.enhance(2.0)

#         # Binarize the image using Otsu's thresholding or a fixed threshold value
#         threshold = 20  # This is an example threshold value that you might need to adjust
#         img_binarized = img_contrast.point(lambda x: 0 if x < threshold else 255, '1')

#         # Optional: Dilate or erode characters if they're too thin or broken using morphology operations.
#         # This step requires conversion to a binary array and use of libraries such as OpenCV or scikit-image.

#         # Optional: Deskewing the image if the text lines are not aligned horizontally may also help.
#         # Use an algorithm to detect text orientation and rotate the image to compensate.

#         # Optional: Remove noise and artifacts that are not part of the text.
#         # This can involve removing small objects, lines, or performing selective blurring.

#         # Append the preprocessed image for OCR
#         new_images.append(img_binarized)

#     return new_images


# def set_tesseract_path():
#     pytesseract.pytesseract.tesseract_cmd = (
#         r"C:\Users\rafael.lins\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
#     )


# set_tesseract_path()


def run_pdf(pdf_binary_data, dpi_value, nlp, idx=0):
    try:
        start_time_decode = time.time()
        pdf_decoded = base64.b64decode(pdf_binary_data["filePDF"])
        end_time_decode = time.time() - start_time_decode
        print(f"Tempo de execução para o decode do base64: {end_time_decode} da nota {idx}")

        pdf_file = PyPDF2.PdfReader(io.BytesIO(pdf_decoded))

        if len(pdf_file.pages) > 5:
            return (
                "Documento inválido, número de páginas acima do limite permitido",
                idx,
                pdf_binary_data["id"],
            )

        start_time_convert = time.time()
        images = convert_from_bytes(pdf_decoded, dpi=dpi_value)
        end_time_convert = time.time() - start_time_convert
        print(
            f"Tempo de execução para a conversão do pdf: {end_time_convert} da nota {idx}"
        )

        start_time_improve = time.time()
        improved_images = melhorar_contraste_e_suavizar(images)
        end_time_improve = time.time() - start_time_improve
        print(
            f"Tempo de execução para a melhoria de imagem: {end_time_improve} da nota {idx}"
        )

        start_time_ocr = time.time()
        text_output = ""
        reader = easyocr.Reader(['pt']) # this needs to run only once to load the model into memory
        for image in improved_images:
            text_output += reader.readtext(np.array(image))
        # for image in improved_images:
            # text_output += pytesseract.image_to_string(image, lang="por", config='--oem 1')
            # text_output += pytesseract.image_to_string(image, lang="por", config='--psm 12 --oem 2')
        end_time_ocr = time.time() - start_time_ocr
        print(f"Tempo de execução para o OCR: {end_time_ocr} da nota {idx}")

        start_time_validate = time.time()
        keywords1 = ["prefeitura", "pref."]
        keywords2 = ["nota fiscal", "nfse", "nfs-e"]
        if not any(keyword in text_output.lower() for keyword in keywords1):
            if not any(phrase in text_output.lower() for phrase in keywords2):
                return (
                    "Documento inválido, documento não é uma nota fiscal.",
                    idx,
                    pdf_binary_data["id"],
                )

        text = strip_accents(format_text(text_output).lower())
        doc = nlp(text)
        nota = {}
        id = pdf_binary_data["id"]
        nota["id"] = id
        fields = {}
        fields["indIntegracao"] = "PDE"
        for i in doc.ents:
            fields[i.label_] = str(i)

        nota["nota"] = fields
        nota["texto"] = text
        # nota = json.dumps(nota["nota"])
        return nota, idx, pdf_binary_data["id"]

    except Exception as e:
        print(e)
        return "Erro ao processar pdf", idx, pdf_binary_data["id"]

def main():
    nlp = spacy.load("src/spacy_model/model-best7")

    with open("src/data/main_data/original_data/all_files.json", "r") as file:
        data = json.load(file)

    # random.shuffle(data)
    data = data[:100]
    output = [""] * len(data)
    # "codigoServico": "1709",
    # "codigoVerificacao": "0186850010871578",
    # "dataEmissaoNFSe": "2022-12-15 00:00:00",
    # "indIntegracao": "PDE",
    # "municipioExecServico": "CORRENTINA ",
    # "numeroNFSe": "1709",
    # "observacao": "Nota criada a partir do PDE - ENSAIOS ELETRICOS EM EPIS EPCS E FERRAMENTAS CONFORME PEDIDO DE COMPRA 1000136 ",
    # "prestador": "07224026000102",
    # "tomador": "07620094000493",
    # "valorServico": "2835.28"
    start_time_convert = time.time()
    with ProcessPoolExecutor() as executor:
        future_to_row = {
            executor.submit(run_pdf, pdf_file, 350, nlp, idx): pdf_file
            for idx, pdf_file in enumerate(data)
        }
        for future in as_completed(future_to_row):
            result = future.result()
            if result is not None:
                try:
                    extracted_text = result[0]
                    idx = result[1]
                    name = result[2]
                    if extracted_text:
                        output[idx] = extracted_text
                    else:
                        output[idx] = None
                except:
                    pass

    # Step 3: Save the response to a JSON file

    output_json_filename = (
        "output_spacy.json"  # Output file name for the second request response
    )
    end_time_convert = time.time() - start_time_convert
    print(f"Tempo de execução: {end_time_convert}")
    # data = json.dumps(output, indent=4, ensure_ascii=False)
    with open(output_json_filename, "w", encoding="utf-8") as outfile:
        json.dump(output, outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()

