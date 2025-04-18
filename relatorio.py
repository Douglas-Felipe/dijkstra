from typing import List, Tuple, Dict

def gerar_relatorio(rota: List[Tuple[str, str, float]], distancia_total: float, pedidos: Dict[str, str]) -> None:
    if not rota:
        print("Nenhuma rota para gerar relatório.")
        return

    print("Relatório da Rota:")
    # Itera sobre cada trecho da rota, desempacotando origem, destino e distância
    for origem, destino, distancia in rota:
        entrega = ""
        for produto, node in pedidos.items():
            # Verifica se o nó do pedido corresponde ao destino atual
            if node == destino:
                entrega = f" (Entrega: {produto})"
                break
        print(f"{origem} - {distancia}km -> {destino}{entrega}")
    print(f"Total: {distancia_total}km")