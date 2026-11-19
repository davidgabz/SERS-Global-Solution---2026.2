import csv
import json
import os
import re
import time
from datetime import datetime


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.arquivo_historico = os.path.join(
            os.path.dirname(base.caminho), "historico.json"
        )
        self.arquivo_csv = os.path.join(
            os.path.dirname(base.caminho), "atendimentos.csv"
        )
        self.historico = []
        self.indices_sessao = []
        self._carregar_historico()

    def _carregar_historico(self):
        try:
            with open(self.arquivo_historico, "r", encoding="utf-8") as arquivo:
                registros = json.load(arquivo)
            if not isinstance(registros, list) or any(
                not isinstance(registro, dict) for registro in registros
            ):
                raise ValueError("O histórico precisa ser uma lista de registros.")
            self.historico = registros
        except FileNotFoundError:
            self.historico = []
        except (OSError, json.JSONDecodeError, ValueError) as erro:
            self.historico = []
            print(f"Não foi possível ler o histórico: {erro}")

    def _salvar_historico(self):
        try:
            os.makedirs(os.path.dirname(self.arquivo_historico), exist_ok=True)
            with open(self.arquivo_historico, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError as erro:
            print(f"Não foi possível salvar o histórico: {erro}")

    def _contem_dados_pessoais(self, texto):
        return "@" in texto or len(re.findall(r"\d", texto)) >= 8

    def registrar(
        self,
        origem,
        pergunta,
        orientacao,
        encontrou,
        ajudou,
        tentativas,
        inicio,
        participante=None,
        modo="terminal",
        perguntas=None,
    ):
        if self._contem_dados_pessoais(pergunta):
            return

        if perguntas is None:
            perguntas = [pergunta]
        perguntas = [p for p in perguntas if isinstance(p, str) and p.strip()]
        registro = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "origem": origem,
            "pergunta": pergunta,
            "perguntas": perguntas,
            "id_orientacao": orientacao.id if orientacao else None,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1),
            "facilidade": None,
            "participante": participante,
            "modo": modo,
        }
        self.historico.append(registro)
        self.indices_sessao.append(len(self.historico) - 1)
        self._salvar_historico()

    def _perguntar_se_ajudou(self):
        while True:
            resposta = input(
                "Essa orientação respondeu sua dúvida? (s/n, 0 para voltar): "
            ).strip().lower()
            if resposta == "s":
                return True
            if resposta == "n":
                return False
            if resposta == "0":
                return None
            print("Resposta inválida. Digite s, n ou 0.")

    def perguntar(self):
        if not self.base.orientacoes:
            print("A base de conhecimento está vazia ou indisponível.")
            return

        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""
        perguntas = []

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                if tentativas > 0:
                    self.registrar(
                        "pergunta", ultima_pergunta, None, False, None,
                        tentativas, inicio, perguntas=perguntas
                    )
                return
            if not pergunta:
                print("Digite uma pergunta ou 0 para voltar.")
                continue
            if self._contem_dados_pessoais(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            ultima_pergunta = pergunta
            perguntas.append(pergunta)
            resultados = self.base.buscar(pergunta)

            if not resultados or resultados[0][0] < 3:
                print(
                    "Não encontrei uma orientação confiável. "
                    "Tente outras palavras ou consulte as categorias no menu."
                )
                continue

            pontos, orientacao = resultados[0]
            confianca = "ALTA" if pontos >= 6 else "MÉDIA"
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            orientacao.exibir()

            alternativas = [
                (nota, outra) for nota, outra in resultados[1:]
                if nota >= 3
            ][:2]
            if alternativas:
                print("Outras orientações relacionadas:")
                for nota, outra in alternativas:
                    print(f"  - {outra.titulo} ({nota} pontos)")

            ajudou = self._perguntar_se_ajudou()
            self.registrar(
                "pergunta", pergunta, orientacao, True, ajudou,
                tentativas, inicio, perguntas=perguntas
            )
            return

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Nenhuma categoria disponível.")
            return

        inicio = time.time()
        while True:
            print("\nCATEGORIAS")
            for numero, categoria in enumerate(categorias, 1):
                print(f"{numero} - {categoria}")
            print("0 - Voltar")
            escolha = input("Escolha uma categoria: ").strip()
            if escolha == "0":
                return
            if escolha not in [str(numero) for numero in range(1, len(categorias) + 1)]:
                print("Opção inválida.")
                continue

            categoria = categorias[int(escolha) - 1]
            orientacoes = self.base.por_categoria(categoria)
            while True:
                print(f"\n{categoria.upper()}")
                for numero, orientacao in enumerate(orientacoes, 1):
                    print(f"{numero} - {orientacao.titulo}")
                print("0 - Voltar")
                escolha_orientacao = input("Escolha uma orientação: ").strip()
                if escolha_orientacao == "0":
                    break
                if escolha_orientacao not in [
                    str(numero) for numero in range(1, len(orientacoes) + 1)
                ]:
                    print("Opção inválida.")
                    continue

                orientacao = orientacoes[int(escolha_orientacao) - 1]
                print("\nConfiança: não se aplica (seleção direta por categoria).")
                orientacao.exibir()
                ajudou = self._perguntar_se_ajudou()
                self.registrar(
                    "categoria", orientacao.titulo, orientacao, True,
                    ajudou, 1, inicio, perguntas=[orientacao.titulo]
                )
                inicio = time.time()

    def resumo_indicadores(self, modo=None):
        """Calcula os indicadores obrigatorios; opcionalmente filtra o modo."""
        registros = [
            item for item in self.historico
            if modo is None or item.get("modo") == modo
        ]
        total = len(registros)
        encontrados = [item for item in registros if item.get("encontrou")]
        avaliados = [item for item in encontrados if item.get("ajudou") is not None]
        ajudaram = sum(item.get("ajudou") is True for item in avaliados)
        notas = [
            item["facilidade"] for item in registros
            if isinstance(item.get("facilidade"), int)
            and 1 <= item["facilidade"] <= 5
        ]
        sem_solucao = list(dict.fromkeys(
            item.get("pergunta", "") for item in registros
            if not item.get("encontrou") or item.get("ajudou") is False
        ))
        participantes = sorted({
            item["participante"] for item in registros
            if item.get("participante") and item.get("participante") != "OPERADOR"
        })
        perguntas_totais = 0
        registros_formatados = []
        for item in reversed(registros):
            perguntas = item.get("perguntas") or ([item.get("pergunta")] if item.get("pergunta") else [])
            perguntas_limpa = [p for p in perguntas if isinstance(p, str) and p.strip()]
            perguntas_totais += len(perguntas_limpa) if perguntas_limpa else int(item.get("tentativas") or 0)
            novo = dict(item)
            novo["perguntas"] = perguntas_limpa
            registros_formatados.append(novo)
        return {
            "total": total,
            "participantes": len(participantes),
            "encontrados": len(encontrados),
            "perguntas_totais": perguntas_totais,
            "resposta_encontrada_pct": round(100 * len(encontrados) / total, 1) if total else None,
            "taxa_acerto_pct": round(100 * ajudaram / len(avaliados), 1) if avaliados else None,
            "tempo_medio_segundos": round(
                sum(float(item.get("tempo_segundos") or 0) for item in encontrados) / len(encontrados), 1
            ) if encontrados else None,
            "tentativas_medias": round(
                sum(int(item.get("tentativas") or 0) for item in registros) / total, 1
            ) if total else None,
            "facilidade_media": round(sum(notas) / len(notas), 1) if notas else None,
            "notas_coletadas": len(notas),
            "sem_solucao": sem_solucao,
            "registros": registros_formatados,
        }

    def indicadores(self):
        dados = self.resumo_indicadores()
        print("\nINDICADORES DE ATENDIMENTO")
        print(f"Total de atendimentos: {dados['total']}")
        if not dados["total"]:
            print("Nao ha atendimentos suficientes para calcular indicadores.")
            return
        print(f"Total de perguntas válidas: {dados['perguntas_totais']}")
        print(f"Resposta encontrada: {dados['resposta_encontrada_pct']:.1f}%")
        if dados["taxa_acerto_pct"] is None:
            print("Taxa de acerto (ajudou): sem avaliacoes")
        else:
            print(f"Taxa de acerto (ajudou): {dados['taxa_acerto_pct']:.1f}%")
        if dados["tempo_medio_segundos"] is None:
            print("Tempo medio para encontrar: sem respostas encontradas")
        else:
            print(f"Tempo medio para encontrar: {dados['tempo_medio_segundos']:.1f} s")
        print(f"Tentativas por atendimento: {dados['tentativas_medias']:.1f}")
        if dados["facilidade_media"] is None:
            print("Facilidade de uso (1 a 5): sem avaliacoes")
        else:
            print(f"Facilidade de uso (1 a 5): {dados['facilidade_media']:.1f}")
        print("Duvidas sem solucao:")
        for pergunta in dados["sem_solucao"]:
            print(f"  - {pergunta}")
        if not dados["sem_solucao"]:
            print("  Nenhuma registrada.")

    def avaliar_facilidade(self):
        while True:
            resposta = input(
                "\nDe 1 a 5, qual foi a facilidade de uso? "
                "(0 para voltar ao menu): "
            ).strip()
            if resposta == "0":
                return False
            if resposta in ("1", "2", "3", "4", "5"):
                if self.indices_sessao:
                    ultimo = self.indices_sessao[-1]
                    self.historico[ultimo]["facilidade"] = int(resposta)
                    self._salvar_historico()
                else:
                    print("Nota recebida. Não houve atendimento nesta sessão para registrá-la.")
                return True
            print("Digite uma nota entre 1 e 5 ou 0 para voltar.")

    def exportar_csv(self):
        campos = [
            "data", "origem", "pergunta", "perguntas", "id_orientacao", "encontrou",
            "ajudou", "tentativas", "tempo_segundos", "facilidade",
            "participante", "modo"
        ]
        try:
            os.makedirs(os.path.dirname(self.arquivo_csv), exist_ok=True)
            with open(self.arquivo_csv, "w", encoding="utf-8-sig", newline="") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos)
                escritor.writeheader()
                for registro in self.historico:
                    linha = {}
                    for campo in campos:
                        valor = registro.get(campo)
                        if campo == "perguntas" and isinstance(valor, list):
                            valor = " | ".join(valor)
                        linha[campo] = "" if valor is None else valor
                    escritor.writerow(linha)
            print(f"Atendimentos exportados para {self.arquivo_csv}")
        except OSError as erro:
            print(f"Não foi possível exportar o CSV: {erro}")
