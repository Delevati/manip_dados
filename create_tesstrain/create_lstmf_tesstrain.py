import os
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def processar_box(box_file, output_folder):
    if box_file.endswith(".box"):
        nome_base = os.path.splitext(box_file)[0]
        caminho_box = os.path.join(output_folder, box_file)
        comando_lstmf = f"mftraining -F {nome_base}.lstmf -U unicharset {caminho_box}"
        os.system(comando_lstmf)

def gerar_lstmf_em_paralelo(output_folder, num_cores=4):
    box_files = [box_file for box_file in os.listdir(output_folder) if box_file.endswith(".box")]

    with ProcessPoolExecutor(max_workers=num_cores) as executor, tqdm(total=len(box_files), desc="Gerando arquivos .lstmf") as pbar:
        for _ in executor.map(processar_box, box_files, [output_folder] * len(box_files)):
            pbar.update(1)

if __name__ == "__main__":
    output_folder = "/home/ubuntu/OCR/manip_dados/create_box_tesstrain/.box"

    gerar_lstmf_em_paralelo(output_folder)
