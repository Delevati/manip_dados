import os
import shutil
from tqdm import tqdm

def copy_tif_files(source_folder, destination_folder):
    # Garanta que a pasta de destino exista
    os.makedirs(destination_folder, exist_ok=True)

    # Liste todos os arquivos .tif na pasta de origem
    tif_files = [f for f in os.listdir(source_folder) if f.endswith('.tif')]

    # Use tqdm para obter barras de progresso
    for tif_file in tqdm(tif_files, desc="Copiando arquivos .tif"):
        source_path = os.path.join(source_folder, tif_file)
        destination_path = os.path.join(destination_folder, tif_file)

        shutil.copy2(source_path, destination_path)

if __name__ == "__main__":
    # Substitua esses caminhos pelos caminhos relevantes
    source_folder = "/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/por_vert-ground-truth"
    destination_folder = "/home/ubuntu/OCR/manip_dados/create_box_tesstrain/.tif"

    copy_tif_files(source_folder, destination_folder)
