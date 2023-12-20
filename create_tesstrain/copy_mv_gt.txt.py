import os
import shutil
from tqdm import tqdm

def copy_gt_files(source_folder, destination_folder):
    # Garanta que a pasta de  exista
    os.makedirs(destination_folder, exist_ok=True)

    # Liste todos os arquivos .gt.txt na pasta de origem
    gt_files = [f for f in os.listdir(source_folder) if f.endswith('.gt.txt')]

    # Use tqdm para obter barras de progresso
    for gt_file in tqdm(gt_files, desc="Copiando arquivos .gt.txt"):
        source_path = os.path.join(source_folder, gt_file)
        destination_path = os.path.join(destination_folder, gt_file)

        shutil.copy2(source_path, destination_path)

if __name__ == "__main__":
    # Substitua esses caminhos pelos caminhos relevantes
    source_folder = "/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/por_vert-ground-truth"
    destination_folder = "/home/ubuntu/OCR/manip_dados/create_box_tesstrain/merge"

    copy_gt_files(source_folder, destination_folder)

#make unicharset lists proto-model training

