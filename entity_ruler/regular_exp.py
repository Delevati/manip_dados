from html import entities
import re


def parte_um(text):
    # Padrões de data
    padrao_data_dd_mm_aaaa = r'\b\d{2}/\d{2}/\d{4}\b'
    padrao_data_aaaa_dd_mm = r'\b\d{4}/\d{2}/\d{2}\b'

    # Padrão de valor em R$
    padrao_valor_r = r'\b\d*,\d{2}|\b\d*.\d*,\d{2}'
    # Busca por padrões
    resultados_data_dd_mm_aaaa = re.findall(padrao_data_dd_mm_aaaa, text)
    resultados_data_aaaa_dd_mm = re.findall(padrao_data_aaaa_dd_mm, text)
    resultados_valor_r = re.findall(padrao_valor_r, text)

    try:
        maior_valor = max(resultados_valor_r, key=lambda x: float(x.replace('.', '').replace(',', '').replace(' ', '')), default=None)
    except:
        maior_valor = 0
        print("Valor não encontrado.")

    new_text = text.replace(" ", "")
    resultador_cnpj = re.findall(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", new_text)
    return resultados_data_aaaa_dd_mm, resultados_data_dd_mm_aaaa, maior_valor, resultador_cnpj

