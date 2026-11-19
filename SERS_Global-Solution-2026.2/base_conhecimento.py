import json
import re
import unicodedata

from orientacao import Orientacao


def normalizar(texto):
    texto = texto.lower().strip()
    texto = "".join(
        letra for letra in unicodedata.normalize("NFD", texto)
        if unicodedata.category(letra) != "Mn"
    )
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        campos = (
            "id", "categoria", "titulo", "palavras_chave", "resposta",
            "documentos", "onde", "fonte", "verificado_em"
        )
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                registros = json.load(arquivo)

            if not isinstance(registros, list):
                raise ValueError("A base deve ser uma lista de orientações.")

            orientacoes = []
            for registro in registros:
                if not isinstance(registro, dict) or any(
                    campo not in registro for campo in campos
                ):
                    raise ValueError("Há um registro sem os campos obrigatórios.")
                campos_texto = ("categoria", "titulo", "resposta", "onde", "fonte", "verificado_em")
                if not isinstance(registro["id"], int) or any(
                    not isinstance(registro[campo], str) for campo in campos_texto
                ):
                    raise ValueError("Há um registro com tipos de dados inválidos.")
                if not isinstance(registro["palavras_chave"], list) or not all(
                    isinstance(palavra, str) for palavra in registro["palavras_chave"]
                ) or not isinstance(registro["documentos"], list) or not all(
                    isinstance(documento, str) for documento in registro["documentos"]
                ):
                    raise ValueError("Palavras-chave e documentos devem ser listas de textos.")
                orientacoes.append(Orientacao(registro))

            self.orientacoes = orientacoes
            return True
        except (OSError, json.JSONDecodeError, ValueError, TypeError) as erro:
            self.orientacoes = []
            print(f"Não foi possível carregar a base de conhecimento: {erro}")
            return False

    def categorias(self):
        return sorted({orientacao.categoria for orientacao in self.orientacoes})

    def por_categoria(self, categoria):
        return [
            orientacao for orientacao in self.orientacoes
            if orientacao.categoria == categoria
        ]

    def pontuar(self, pergunta, orientacao):
        pergunta_normalizada = normalizar(pergunta)
        titulo_normalizado = normalizar(orientacao.titulo)
        pontos = 0

        for palavra_chave in orientacao.palavras_chave:
            chave = normalizar(palavra_chave)
            if chave.strip() and chave in pergunta_normalizada:
                pontos += 3

        for palavra in set(pergunta_normalizada.split()):
            if len(palavra) >= 4 and f" {palavra} " in titulo_normalizado:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = [
            (self.pontuar(pergunta, orientacao), orientacao)
            for orientacao in self.orientacoes
        ]
        return sorted(resultados, key=lambda item: (-item[0], item[1].id))
