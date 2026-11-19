from pathlib import Path

from assistente import Assistente
from base_conhecimento import BaseConhecimento


def main():
    caminho = Path(__file__).resolve().parent / "data" / "base_conhecimento.json"
    base = BaseConhecimento(str(caminho))
    base.carregar()
    assistente = Assistente("Citizen Assist AI - Energia (SERS)", base)

    while True:
        print(f"\n===== {assistente.nome} =====")
        print("1 - Digitar uma dúvida")
        print("2 - Navegar por categorias")
        print("3 - Ver indicadores")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "0":
            if assistente.avaliar_facilidade():
                assistente.indicadores()
                assistente.exportar_csv()
                print("Até logo!")
                break
        else:
            print("Opção inválida. Escolha 0, 1, 2 ou 3.")


if __name__ == "__main__":
    main()
