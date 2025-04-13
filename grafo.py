from typing import Dict, Set

class Grafo:
    def __init__(self) -> None:
        self.nodes: Set[str] = set()  # Conjunto de nodes (strings)
        self.ligacoes: Dict[str, Dict[str, float]] = {}  # node -> {vizinho: distância}

    def adicionar_node(self, node: str) -> None:
        if node not in self.nodes:
            self.nodes.add(node)
            self.ligacoes[node] = {}
        else:
            print(f"Node {node} já existe.")

    def remover_node(self, node: str) -> None:
        if node == "Centro de Distribuição":
            print("Não é possível remover o Centro de Distribuição.")
            return
        if node in self.nodes:
            self.nodes.remove(node)
            del self.ligacoes[node]
            for n in self.ligacoes:
                if node in self.ligacoes[n]:
                    del self.ligacoes[n][node]
        else:
            print(f"Node {node} não encontrado.")

    def adicionar_ligacao(self, node1: str, node2: str, distancia: float) -> None:
        if node1 not in self.nodes or node2 not in self.nodes:
            print("Um ou ambos os nodes não existem.")
            return
        self.ligacoes[node1][node2] = distancia
        self.ligacoes[node2][node1] = distancia  # Ligações bidirecionais

    def editar_node(self, node_antigo: str, node_novo: str) -> None:
        if node_antigo == "Centro de Distribuição":
            print("Não é possível editar o Centro de Distribuição.")
            return
        if node_antigo in self.nodes:
            self.nodes.remove(node_antigo)
            self.nodes.add(node_novo)
            self.ligacoes[node_novo] = self.ligacoes.pop(node_antigo)
            for n in self.ligacoes:
                if node_antigo in self.ligacoes[n]:
                    self.ligacoes[n][node_novo] = self.ligacoes[n].pop(node_antigo)
        else:
            print(f"Node {node_antigo} não encontrado.")