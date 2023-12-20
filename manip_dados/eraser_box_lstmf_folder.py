import os

def apagar_arquivos_com_extensao(diretorio, extensoes):
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(tuple(extensoes)):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            os.remove(caminho_arquivo)
            print(f"Arquivo {caminho_arquivo} removido com sucesso.")

# Diretório onde os arquivos estão localizados
diretorio_alvo = "/home/ubuntu/OCR/manip_dados/pdfs/PDFS"

# Extensões dos arquivos que você deseja excluir
extensoes_a_excluir = (".png~", ".png~~", ".png~~~")

# Chamando a função para apagar os arquivos
apagar_arquivos_com_extensao(diretorio_alvo, extensoes_a_excluir)
