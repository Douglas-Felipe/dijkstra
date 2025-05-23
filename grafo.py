from typing import Dict, Set
import networkx as nx
import matplotlib.pyplot as plt
import json

JSON_CACHE = "grafo.json"

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
            # Itera sobre todos os nós restantes no dicionário de ligações.
            for n in self.ligacoes:
                # Verifica se o nó removido existe como vizinho do nó atual 'n'.
                if node in self.ligacoes[n]:
                    # Remove a ligação do nó 'n' para o nó removido.
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
                # Verifica se o nó antigo era um vizinho do nó 'n'.
                if node_antigo in self.ligacoes[n]:
                    # Atualiza a referência: remove a ligação para o nó antigo e adiciona para o nó novo, mantendo a distância.
                    self.ligacoes[n][node_novo] = self.ligacoes[n].pop(node_antigo)
        else:
            print(f"Node {node_antigo} não encontrado.")

    def exibir_grafo(self) -> None:
        if not self.nodes:
            print("O grafo está vazio.")
            return
        
        G = nx.Graph()
        G.add_nodes_from(self.nodes)
        
        # Conjunto para rastrear pares de nós já adicionados como arestas, evitando duplicatas na visualização
        # (já que nosso dicionário `ligacoes` armazena a ligação em ambas as direções).
        exibidos = set()
        for node in self.nodes:
            # Itera sobre os vizinhos e distâncias do nó atual.
            for vizinho, distancia in self.ligacoes[node].items():
                # Cria uma tupla ordenada dos nós para representar a aresta de forma única.
                par = tuple(sorted([node, vizinho]))
                if par not in exibidos:
                    exibidos.add(par)
                    G.add_edge(node, vizinho, weight=distancia)
        
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 8)) 
        
        # Define as cores dos nós: vermelho para o Centro de Distribuição, azul claro para os outros.
        node_colors = ['red' if node == "Centro de Distribuição" else 'lightblue' for node in G.nodes()]
        
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, 
                font_size=10, font_weight='bold', edge_color='gray')
        
        # Obtém os pesos das arestas para exibição.
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        
        plt.title("Visualização do Grafo de Entregas")
        plt.show()

    def salvar_json(self) -> None:
        grafo_data = {
            "nodes": list(self.nodes),
            "ligacoes": self.ligacoes
        }
        with open(JSON_CACHE, 'w') as f:
            json.dump(grafo_data, f, indent=4)
        print(f"Grafo salvo em {JSON_CACHE}")

    def carregar_json(self) -> None:
        try:
            with open(JSON_CACHE, 'r') as f:
                grafo_data = json.load(f)
            self.nodes = set(grafo_data["nodes"])
            self.ligacoes = {node: {vizinho: float(dist) for vizinho, dist in conexoes.items()} 
                            for node, conexoes in grafo_data["ligacoes"].items()}
            print(f"Grafo carregado de {JSON_CACHE}")
        except FileNotFoundError:
            print(f"Arquivo {JSON_CACHE} não encontrado.")
        except Exception as e:
            print(f"Erro ao carregar o grafo de {JSON_CACHE}: {e}")
