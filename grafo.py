from typing import Dict, Set
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self) -> None:
        self.nodes: Set[str] = set()
        self.ligacoes: Dict[str, Dict[str, float]] = {}

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
        self.ligacoes[node2][node1] = distancia

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

    def exibir_grafo(self) -> None:
        if not self.nodes:
            print("O grafo está vazio.")
            return

        # Cria um grafo NetworkX
        G = nx.Graph()

        # Adiciona os nodes ao grafo NetworkX
        G.add_nodes_from(self.nodes)

        # Adiciona as arestas com pesos (distâncias)
        exibidos = set()  # Evita duplicatas nas ligações bidirecionais
        for node in self.nodes:
            for vizinho, distancia in self.ligacoes[node].items():
                par = tuple(sorted([node, vizinho]))
                if par not in exibidos:
                    exibidos.add(par)
                    G.add_edge(node, vizinho, weight=distancia)

        # Configura o layout do grafo (spring layout é um bom padrão)
        pos = nx.spring_layout(G)

        # Desenha o grafo
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # Destaca o Centro de Distribuição com uma cor diferente
        node_colors = ['red' if node == "Centro de Distribuição" else 'lightblue' for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)

        # Exibe o grafo
        plt.title("Visualização do Grafo de Entregas")
        plt.show()