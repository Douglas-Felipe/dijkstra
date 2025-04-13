import heapq
from typing import Dict, Tuple, List, Set, Optional

from grafo import Grafo

def dijkstra(grafo: Grafo, inicio: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    distancias: Dict[str, float] = {node: float('inf') for node in grafo.nodes}
    distancias[inicio] = 0
    predecessores: Dict[str, Optional[str]] = {node: None for node in grafo.nodes}
    fila_prioridade: List[Tuple[float, str]] = [(0, inicio)]

    while fila_prioridade:
        distancia_atual, node_atual = heapq.heappop(fila_prioridade)

        if distancia_atual > distancias[node_atual]:
            continue

        for vizinho, peso in grafo.ligacoes[node_atual].items():
            distancia = distancia_atual + peso
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                predecessores[vizinho] = node_atual
                heapq.heappush(fila_prioridade, (distancia, vizinho))

    return distancias, predecessores

def calcular_rota(grafo: 'Grafo', pedidos: Dict[str, str]) -> Tuple[List[Tuple[str, str, float]], float]:
    if not pedidos:
        return [], 0

    inicio = "Centro de Distribuição"
    nodes_entrega: Set[str] = set(pedidos.values())

    # Lista para armazenar a rota completa
    rota: List[Tuple[str, str, float]] = []
    distancia_total: float = 0
    node_atual: str = inicio

    while nodes_entrega:
        # Calcula o caminho mais curto do node atual para todos os outros usando Dijkstra
        distancias, predecessores = dijkstra(grafo, node_atual)

        # Encontra o node de entrega mais próximo que ainda não foi visitado
        proximos = {node: distancias[node] for node in nodes_entrega if distancias[node] < float('inf')}
        if not proximos:
            print("Não é possível alcançar todos os nodes de entrega.")
            return [], 0

        proximo_node = min(proximos, key=proximos.get)

        # Reconstrói o caminho do node atual até o próximo node de entrega
        def reconstruir_caminho(node: str) -> List[str]:
            caminho: List[str] = []
            while node is not None:
                caminho.append(node)
                node = predecessores[node]
            return caminho[::-1]

        caminho = reconstruir_caminho(proximo_node)

        # Adiciona os segmentos do caminho à rota
        for i in range(len(caminho) - 1):
            node_origem = caminho[i]
            node_destino = caminho[i + 1]
            distancia = grafo.ligacoes[node_origem][node_destino]
            rota.append((node_origem, node_destino, distancia))
            distancia_total += distancia

        # Marca o node como visitado e atualiza o node atual
        nodes_entrega.remove(proximo_node)
        node_atual = proximo_node

    return rota, distancia_total