from typing import Dict
import json

PEDIDOS_JSON = "pedidos.json"


class Pedidos:
    def __init__(self) -> None:
        self.pedidos: Dict[str, str] = {}

    def adicionar_pedido(self, produto: str, node: str) -> None:
        if node in self.pedidos.values():
            print(f"O node {node} já tem um produto associado.")
            return
        self.pedidos[produto] = node

    def remover_pedido(self, produto: str) -> None:
        if produto in self.pedidos:
            del self.pedidos[produto]
        else:
            print(f"Produto {produto} não encontrado.")

    def listar_pedidos(self) -> None:
        for produto, node in self.pedidos.items():
            print(f"Produto: {produto} -> Node: {node}")

    def salvar_json(self) -> None:
        with open(PEDIDOS_JSON, 'w') as f:
            json.dump(self.pedidos, f, indent=4)
        print(f"Pedidos salvos em {PEDIDOS_JSON}")

    def carregar_json(self) -> None:
        try:
            with open(PEDIDOS_JSON, 'r') as f:
                self.pedidos = json.load(f)
            print(f"Pedidos carregados de {PEDIDOS_JSON}")
        except FileNotFoundError:
            print(f"Arquivo {PEDIDOS_JSON} não encontrado.")
        except Exception as e:
            print(f"Erro ao carregar os pedidos: {e}")