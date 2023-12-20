import os

def apagar_arquivos_vazios(path_pasta):
    for nome_arquivo in os.listdir(path_pasta):
        if nome_arquivo.endswith('.txt'):
            caminho_txt = os.path.join(path_pasta, nome_arquivo)
            caminho_tif = os.path.join(path_pasta, nome_arquivo.replace('.gt.txt', '.tif'))

            # Verifique se o arquivo de texto está vazio
            if os.path.getsize(caminho_txt) == 0:
                print(f"O arquivo de texto '{caminho_txt}' está vazio. Excluindo...")

                # Exclua o arquivo de texto
                os.remove(caminho_txt)

                # Verifique se o arquivo TIFF existe e, se existir, exclua-o
                if os.path.exists(caminho_tif):
                    print(f"Excluindo arquivo TIFF associado: '{caminho_tif}'")
                    os.remove(caminho_tif)

def main():
    path_pasta = '/home/ubuntu/OCR/tesstrain_2rd/tesstrain/data/por_vert-ground-truth'  # Substitua pelo caminho real da sua pasta
    apagar_arquivos_vazios(path_pasta)

if __name__ == "__main__":
    main()
