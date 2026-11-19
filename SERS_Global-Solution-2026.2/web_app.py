"""Interface web do Citizen Assist AI Energia - SERS.

Execução alternativa pelo terminal:
    python3 main.py

Interface web local:
    python3 web_app.py
"""

import argparse
import json
import re
import secrets
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from assistente import Assistente
from base_conhecimento import BaseConhecimento

PASTA = Path(__file__).resolve().parent
ARQUIVO_HTML = PASTA / "web" / "index.html"
ROTAS_HTML = {"/", "/index.html", "/usuario", "/operador"}


class Servidor(HTTPServer):
    def __init__(self, endereco):
        super().__init__(endereco, Requisicoes)
        base = BaseConhecimento(str(PASTA / "data" / "base_conhecimento.json"))
        base.carregar()
        self.assistente = Assistente("Citizen Assist AI - Energia (SERS)", base)
        self.sessoes = {}

    def sessao(self, modo, participante):
        chave = (modo, participante)
        if chave not in self.sessoes:
            self.sessoes[chave] = {
                "inicio": None,
                "tentativas": 0,
                "ultima_pergunta": "",
                "perguntas": [],
                "pendente": None,
                "origem": "pergunta",
            }
        return self.sessoes[chave]

    def zerar_sessao(self, modo, participante):
        self.sessoes.pop((modo, participante), None)


class Requisicoes(BaseHTTPRequestHandler):
    def log_message(self, formato, *args):
        pass

    def enviar_json(self, dados, status=200):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(corpo)

    def enviar_html(self, caminho):
        try:
            corpo = ARQUIVO_HTML.read_bytes()
        except OSError:
            self.enviar_json({"erro": "Interface HTML não encontrada."}, 500)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(corpo)

    def enviar_erro(self, mensagem, status=400):
        self.enviar_json({"erro": mensagem}, status)

    def ler_json(self):
        tamanho = int(self.headers.get("Content-Length", "0"))
        if not 0 < tamanho <= 20000:
            raise ValueError("Requisição vazia ou muito grande.")
        try:
            dados = json.loads(self.rfile.read(tamanho))
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise ValueError("Dados de entrada inválidos.")
        if not isinstance(dados, dict):
            raise ValueError("Formato de dados inválido.")
        return dados

    def contexto(self, dados):
        modo = dados.get("modo")
        participante = dados.get("participante")
        if modo not in ("teste", "operador"):
            raise ValueError("Modo inválido.")
        if modo == "operador":
            participante = "OPERADOR"
        elif not isinstance(participante, str) or not re.fullmatch(r"P-[A-F0-9]{6}", participante):
            raise ValueError("Identificador de participante inválido.")
        return modo, participante, self.server.sessao(modo, participante)

    @staticmethod
    def resumir_orientacao(orientacao):
        return {
            "id": orientacao.id,
            "categoria": orientacao.categoria,
            "titulo": orientacao.titulo,
            "resposta": orientacao.resposta,
            "documentos": orientacao.documentos,
            "onde": orientacao.onde,
            "fonte": orientacao.fonte,
            "verificado_em": orientacao.verificado_em,
        }

    def pacote_indicadores(self):
        assistente = self.server.assistente
        return {
            "teste": assistente.resumo_indicadores(modo="teste"),
            "operador": assistente.resumo_indicadores(modo="operador"),
            "geral": assistente.resumo_indicadores(modo=None),
        }

    def do_GET(self):
        caminho = self.path.split("?", 1)[0]
        if caminho in ROTAS_HTML:
            self.enviar_html(caminho)
            return
        if caminho == "/api/base":
            categorias = self.server.assistente.base.categorias()
            self.enviar_json({
                "nome": self.server.assistente.nome,
                "categorias": [
                    {
                        "nome": categoria,
                        "orientacoes": [
                            {"id": o.id, "titulo": o.titulo}
                            for o in self.server.assistente.base.por_categoria(categoria)
                        ],
                    }
                    for categoria in categorias
                ],
            })
            return
        if caminho == "/api/indicadores":
            self.enviar_json(self.pacote_indicadores())
            return
        if caminho == "/api/exportar":
            self.server.assistente.exportar_csv()
            try:
                corpo = Path(self.server.assistente.arquivo_csv).read_bytes()
            except OSError:
                self.enviar_erro("Não foi possível exportar o CSV.", 500)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="atendimentos.csv"')
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(corpo)
            return
        self.enviar_erro("Página não encontrada.", 404)

    def do_POST(self):
        try:
            dados = self.ler_json()
            caminho = self.path.split("?", 1)[0]
            assistente = self.server.assistente

            if caminho == "/api/novo-participante":
                self.enviar_json({"participante": "P-" + secrets.token_hex(3).upper()})
                return

            modo, participante, sessao = self.contexto(dados)

            if caminho == "/api/reiniciar":
                self.server.zerar_sessao(modo, participante)
                self.enviar_json({"ok": True})
                return

            if caminho == "/api/perguntar":
                pergunta = dados.get("pergunta")
                if not isinstance(pergunta, str) or not pergunta.strip():
                    raise ValueError("Digite uma pergunta antes de enviar.")
                pergunta = pergunta.strip()
                if len(pergunta) > 500:
                    raise ValueError("Pergunta muito longa. Use até 500 caracteres.")
                if assistente._contem_dados_pessoais(pergunta):
                    raise ValueError("Não digite nome, CPF, telefone ou e-mail. Reformule a pergunta.")
                if sessao["pendente"] is not None:
                    raise ValueError("Avalie a orientação anterior antes de continuar.")
                if not assistente.base.orientacoes:
                    raise ValueError("A base de conhecimento está indisponível.")

                if sessao["inicio"] is None:
                    sessao["inicio"] = time.time()
                sessao["tentativas"] += 1
                sessao["ultima_pergunta"] = pergunta
                sessao["perguntas"].append(pergunta)
                sessao["origem"] = "pergunta"

                resultados = assistente.base.buscar(pergunta)
                if not resultados or resultados[0][0] < 3:
                    self.enviar_json({
                        "encontrou": False,
                        "tentativas": sessao["tentativas"],
                        "mensagem": "Ainda não encontrei uma orientação confiável. Tente reformular a pergunta ou abra as categorias.",
                    })
                    return

                pontos, orientacao = resultados[0]
                sessao["pendente"] = orientacao
                alternativas = [
                    {"id": outro.id, "titulo": outro.titulo, "pontos": nota}
                    for nota, outro in resultados[1:] if nota >= 3
                ][:2]
                self.enviar_json({
                    "encontrou": True,
                    "pontos": pontos,
                    "confianca": "ALTA" if pontos >= 6 else "MÉDIA",
                    "orientacao": self.resumir_orientacao(orientacao),
                    "alternativas": alternativas,
                    "tentativas": sessao["tentativas"],
                })
                return

            if caminho == "/api/categoria":
                numero = dados.get("id")
                if type(numero) is not int:
                    raise ValueError("Selecione uma orientação válida.")
                if sessao["pendente"] is not None:
                    raise ValueError("Avalie a orientação anterior antes de continuar.")
                orientacao = next((o for o in assistente.base.orientacoes if o.id == numero), None)
                if orientacao is None:
                    raise ValueError("Orientação não encontrada na base.")

                if sessao["inicio"] is None:
                    sessao["inicio"] = time.time()
                sessao["tentativas"] += 1
                sessao["origem"] = "categoria"
                sessao["ultima_pergunta"] = orientacao.titulo
                sessao["perguntas"].append(orientacao.titulo)
                sessao["pendente"] = orientacao
                self.enviar_json({
                    "encontrou": True,
                    "confianca": "SELEÇÃO DIRETA",
                    "pontos": None,
                    "orientacao": self.resumir_orientacao(orientacao),
                    "alternativas": [],
                    "tentativas": sessao["tentativas"],
                })
                return

            if caminho == "/api/avaliar":
                ajudou = dados.get("ajudou")
                if type(ajudou) is not bool or sessao["pendente"] is None:
                    raise ValueError("Primeiro consulte uma orientação e informe se ajudou ou não.")
                assistente.registrar(
                    sessao["origem"],
                    sessao["ultima_pergunta"],
                    sessao["pendente"],
                    True,
                    ajudou,
                    sessao["tentativas"],
                    sessao["inicio"],
                    participante=(participante if modo == "teste" else "OPERADOR"),
                    modo=modo,
                    perguntas=sessao["perguntas"],
                )
                assistente.exportar_csv()
                self.server.zerar_sessao(modo, participante)
                self.enviar_json({"ok": True, "indicadores": self.pacote_indicadores()})
                return

            if caminho == "/api/sem-solucao":
                if sessao["tentativas"] == 0 or sessao["pendente"] is not None:
                    raise ValueError("Faça uma pergunta sem resposta antes de encerrar como sem solução.")
                assistente.registrar(
                    "pergunta",
                    sessao["ultima_pergunta"],
                    None,
                    False,
                    None,
                    sessao["tentativas"],
                    sessao["inicio"],
                    participante=(participante if modo == "teste" else "OPERADOR"),
                    modo=modo,
                    perguntas=sessao["perguntas"],
                )
                assistente.exportar_csv()
                self.server.zerar_sessao(modo, participante)
                self.enviar_json({"ok": True, "indicadores": self.pacote_indicadores()})
                return

            if caminho == "/api/facilidade":
                nota = dados.get("nota")
                if modo != "teste" or type(nota) is not int or nota not in range(1, 6):
                    raise ValueError("Informe uma nota de facilidade entre 1 e 5.")
                registros_participante = [
                    r for r in assistente.historico
                    if r.get("modo") == "teste" and r.get("participante") == participante
                ]
                if any(r.get("facilidade") is not None for r in registros_participante):
                    raise ValueError("Este participante já avaliou a facilidade de uso.")
                if not registros_participante:
                    raise ValueError("Não há atendimento deste participante para avaliar.")
                registros_participante[-1]["facilidade"] = nota
                assistente._salvar_historico()
                assistente.exportar_csv()
                self.enviar_json({"ok": True, "indicadores": self.pacote_indicadores()})
                return

            self.enviar_erro("Ação não encontrada.", 404)
        except ValueError as erro:
            self.enviar_erro(str(erro), 400)
        except (OSError, TypeError) as erro:
            self.enviar_erro("Não foi possível concluir a operação.", 500)


def main():
    leitor = argparse.ArgumentParser(description="Citizen Assist AI Energia - interface web local")
    leitor.add_argument("--porta", type=int, default=8000)
    leitor.add_argument("--sem-navegador", action="store_true")
    args = leitor.parse_args()
    endereco = f"http://127.0.0.1:{args.porta}"
    try:
        servidor = Servidor(("127.0.0.1", args.porta))
    except OSError as erro:
        print(f"Não foi possível iniciar o servidor: {erro}")
        return
    print(f"Citizen Assist AI Energia | Interface web local: {endereco}")
    print("Página do participante: http://127.0.0.1:{}/usuario".format(args.porta))
    print("Página do operador: http://127.0.0.1:{}/operador".format(args.porta))
    print("Mantenha este terminal aberto. Pressione Ctrl+C para encerrar.")
    if not args.sem_navegador:
        webbrowser.open(endereco)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
