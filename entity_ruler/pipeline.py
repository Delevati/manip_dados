import spacy
from spacy.language import Language
from spacy.pipeline import EntityRuler
import re
import unicodedata

def format_text(text: str) -> str:
    text = text.replace("\n", " ")
    special_characters_pattern = r'[="\\[\]{}();@#&*|ºª./:-]'
    return re.sub(r"\s+", " ", re.sub(special_characters_pattern, "", f"{text}"))
def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )

@Language.component("categorize")
def categorize(doc):
    print(doc.text.capitalize())
    return doc

nlp = spacy.load("pt_core_news_lg")

def regua(text):

    ruler = EntityRuler(nlp)
    patterns = [
        #NUMERO DA NOTA
        {"label": "NFSe", "pattern": [{"TEXT": "numero"}, {"TEXT": "da"}, {"TEXT": "nota"}]},
        {"label": "NFSe", "pattern": [{"TEXT": "numero"}, {"TEXT": "da"}, {"TEXT": "nfse"}]},
        {"label": "NFSe", "pattern": [{"TEXT": "n"}, {"TEXT": "da"}, {"TEXT": "nota"}]},
        {"label": "NFSe", "pattern": [{"TEXT": "n"}, {"TEXT": "da"}, {"TEXT": "nfse"}]},
        # MUNICIPIO DE EXECUCAO
        {"label": "CODIGO_VER", "pattern": "verificacao"},
        #VALOR
        {"label": "Valor", "pattern": [{"TEXT" : {"REGEX": '\$\s*([0-9]{1,3}(?:\.[0-9]{3})*(?:,[0-9]{2}))'}}]},

    ]

    # Adicionar o EntityRuler ao pipeline
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)

    pipes = ['entity_ruler']

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipes]
    nlp.disable_pipes(other_pipes)

    text = strip_accents(format_text(text).lower())

    doc = nlp(text)

    nfse_n = r'^[0-9]'

    labels = ["NFSe", "CODIGO_VER", "Valor"]
    flag_ver = 0
    values = []
    # Encontrar a entidade "CNPJ" e pegar o texto subsequente
    for ent in doc.ents:
        if ent.label_ == 'CNPJ':
            values.append((ent.label_, ent))
        elif ent.label_ == 'CODIGO_VER':
            if not flag_ver:
                flag_ver = 1
                limite_caracteres = 1  # Ajuste o número de caracteres conforme necessário
                texto_posterior = doc[ent.end:ent.end + limite_caracteres].text
                values.append((ent.label_, texto_posterior))
        elif ent.label_ in labels:
            indice_entidade = ent.end
            limite_tokens = 15  # Ajuste o número de tokens conforme necessário
            texto_posterior = doc[indice_entidade:indice_entidade + limite_tokens].text
            values.append((ent.label_, re.sub(r"[^\d]", "", texto_posterior)))

    return values