import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def processar_imagem(imagem, input_folder, output_folder):
    if imagem.endswith(".tif"):
        nome_base = os.path.splitext(imagem)[0]
        caminho_imagem = os.path.join(input_folder, imagem)
        caminho_box = os.path.join(output_folder, nome_base)
        comando_tesseract = f"tesseract {caminho_imagem} {caminho_box} lstmbox"
        os.system(comando_tesseract)

def gerar_box_em_paralelo(input_folder, output_folder, num_cores=4):
    os.makedirs(output_folder, exist_ok=True)

    imagens = [imagem for imagem in os.listdir(input_folder) if imagem.endswith(".tif")]

    with ProcessPoolExecutor(max_workers=num_cores) as executor, tqdm(total=len(imagens), desc="Processando imagens") as pbar:
        futures = [executor.submit(processar_imagem, imagem, input_folder, output_folder) for imagem in imagens]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Aguardando conclusão"):
            pbar.update(1)

if __name__ == "__main__":
    input_folder = "/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/foo-ground-truth"
    output_folder = "/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/foo-ground-truth"

    gerar_box_em_paralelo(input_folder, output_folder)
