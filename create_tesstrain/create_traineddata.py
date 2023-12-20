import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def generate_lstmf_from_box_and_tif(box_folder, tif_folder, output_folder):
    # Garanta que a pasta de saída exista
    os.makedirs(output_folder, exist_ok=True)

    # Liste todos os arquivos .box na pasta de entrada .box
    box_files = [f for f in os.listdir(box_folder) if f.endswith('.box')]

    # Função para processar um único arquivo .box
    def process_file(box_file):
        # Construa os caminhos completos .box e .tif
        box_path = os.path.join(box_folder, box_file)
        tif_path = os.path.join(tif_folder, box_file.replace('.box', '.tif'))
        output_path = os.path.join(output_folder, box_file.replace('.box', ''))

        # Comando para gerar o arquivo .lstmf
        command = f"tesseract {tif_path} {output_path} lstm.train"

        # Execute o comando no terminal
        os.system(command)

    # Use ThreadPoolExecutor para paralelizar o processamento
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Use tqdm para obter barras de progresso
        list(tqdm(executor.map(process_file, box_files), total=len(box_files), desc="Gerando LSTMF"))

if __name__ == "__main__":
    tif_folder = "/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/por_vert-ground-truth"
    box_folder = "/home/ubuntu/OCR/manip_dados/create_box_tesstrain/.box"
    output_folder = "/home/ubuntu/OCR/manip_dados/create_box_tesstrain/.lstmf_.traineddata"

    # Chame a função para gerar os arquivos .lstmf
    generate_lstmf_from_box_and_tif(box_folder, tif_folder, output_folder)
