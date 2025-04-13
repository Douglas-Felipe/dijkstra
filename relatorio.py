from typing import List, Tuple, Dict

def gerar_relatorio(rota: List[Tuple[str, str, float]], distancia_total: float, pedidos: Dict[str, str]) -> None:
    if not rota:
        print("Nenhuma rota para gerar relatório.")
        return

    print("Relatório da Rota:")
    for origem, destino, distancia in rota:
        entrega = ""
        for produto, node in pedidos.items():
            if node == destino:
                entrega = f" (Entrega: {produto})"
                break
        print(f"{origem} - {distancia}km -> {destino}{entrega}")
    print(f"Total: {distancia_total}km")