from typing import Dict

class Pedidos:
    def __init__(self) -> None:
        self.pedidos: Dict[str, str] = {}  # produto -> node

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