import heapq
from typing import Dict, Tuple, List, Set, Optional

from grafo import Grafo

def dijkstra(grafo: Grafo, inicio: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    # Inicializa um dicionário com distâncias infinitas para todos os nós do grafo
    distancias: Dict[str, float] = {node: float('inf') for node in grafo.nodes}
    # Define a distância do nó inicial como 0
    distancias[inicio] = 0
    # Inicializa um dicionário para armazenar o nó predecessor de cada nó no caminho mais curto
    predecessores: Dict[str, Optional[str]] = {node: None for node in grafo.nodes}
    # Cria uma fila de prioridade com tuplas (distância, nó), começando com o nó inicial
    fila_prioridade: List[Tuple[float, str]] = [(0, inicio)]

    # Enquanto houver nós na fila de prioridade
    while fila_prioridade:
        # Remove o nó com menor distância da fila
        distancia_atual, node_atual = heapq.heappop(fila_prioridade)

        # Ignora se encontramos uma distância maior que a já conhecida
        if distancia_atual > distancias[node_atual]:
            continue

        for vizinho, peso in grafo.ligacoes[node_atual].items():
            distancia = distancia_atual + peso
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                predecessores[vizinho] = node_atual
                # Adiciona o vizinho à fila com a nova distância
                heapq.heappush(fila_prioridade, (distancia, vizinho))

    return distancias, predecessores

def calcular_rota(grafo: 'Grafo', pedidos: Dict[str, str]) -> Tuple[List[Tuple[str, str, float]], float]:
    if not pedidos:
        return [], 0

    # Define o ponto de partida como o Centro de Distribuição
    inicio = "Centro de Distribuição"
    # Cria um conjunto com todos os nós de entrega (destinos dos pedidos)
    nodes_entrega: Set[str] = set(pedidos.values())

    rota: List[Tuple[str, str, float]] = []
    distancia_total: float = 0
    node_atual: str = inicio

    while nodes_entrega:
        # Calcula as menores distâncias do nó atual para todos os outros nós
        distancias, predecessores = dijkstra(grafo, node_atual)

        # Cria um dicionário com as distâncias para os nós de entrega ainda não visitados
        proximos = {node: distancias[node] for node in nodes_entrega if distancias[node] < float('inf')}
        if not proximos:
            print("Não é possível alcançar todos os nodes de entrega.")
            return [], 0

        # Escolhe o nó de entrega mais próximo
        proximo_node = min(proximos, key=proximos.get)

        # Função auxiliar para reconstruir o caminho do nó inicial ao nó de entrega
        def reconstruir_caminho(node: str) -> List[str]:
            caminho: List[str] = []
            # Retrocede pelos predecessores até alcançar o nó inicial
            while node is not None:
                caminho.append(node)
                node = predecessores[node]
            # Retorna o caminho na ordem correta (do início ao destino)
            return caminho[::-1]

        caminho = reconstruir_caminho(proximo_node)

        # Adiciona cada segmento do caminho à rota
        for i in range(len(caminho) - 1):
            node_origem = caminho[i]
            node_destino = caminho[i + 1]
            # Obtém a distância entre os nós consecutivos
            distancia = grafo.ligacoes[node_origem][node_destino]
            rota.append((node_origem, node_destino, distancia))
            distancia_total += distancia

        # Remove o nó de entrega visitado do conjunto
        nodes_entrega.remove(proximo_node)
        # Atualiza o nó atual para o nó de entrega recém-visitado
        node_atual = proximo_node

    return rota, distancia_total