import os
import shutil
from tqdm import tqdm

def merge_folders(src_folders, dest_folder):
    # Crie a pasta de destino se não existir
    os.makedirs(dest_folder, exist_ok=True)

    # Itere sobre as pastas de origem
    for src_folder in src_folders:
        # Liste todos os arquivos na pasta de origem
        files = os.listdir(src_folder)

        # Use tqdm para obter barras de progresso
        for file in tqdm(files, desc=f"Copiando arquivos de {src_folder} para {dest_folder}"):
            src_path = os.path.join(src_folder, file)
            dest_path = os.path.join(dest_folder, file)

            # Use shutil.copy2 para preservar metadados
            shutil.copy2(src_path, dest_path)

if __name__ == "__main__":
    # Substitua esses caminhos pelos caminhos relevantes
    box_folder = "/home/ubuntu/OCR/manip_dados/create_box_tesstrain/.box"
    # lstm_folder = "/home/ubuntu/OCR/manip_dados/create_box_tesstrain/.lstmf_.traineddata"
    # tif_folder = "/home/ubuntu/OCR/manip_dados/create_box_tesstrain/.tif"
    merge_folder = "/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/foo-ground-truth"

    # Chame a função para mesclar os arquivos
    # merge_folders([box_folder, lstm_folder, tif_folder], merge_folder)
    merge_folders([box_folder], merge_folder)
