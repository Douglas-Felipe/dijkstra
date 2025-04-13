import questionary
from grafo import Grafo
from pedidos import Pedidos
from rota import calcular_rota
from relatorio import gerar_relatorio
from typing import List, Tuple

def menu() -> None:
    grafo: Grafo = Grafo()
    grafo.adicionar_node("Centro de Distribuição")
    pedidos: Pedidos = Pedidos()

    while True:
        opcao: str = questionary.select(
            "Escolha uma opção:",
            choices=[
                "Adicionar node",
                "Remover node",
                "Editar node",
                "Adicionar ligação",
                "Adicionar pedido",
                "Remover pedido",
                "Listar pedidos",
                "Calcular rota e gerar relatório",
                "Sair"
            ]
        ).ask()

        if opcao == "Adicionar node":
            node: str = questionary.text("Nome do node:").ask()
            grafo.adicionar_node(node)
            print(f"Node '{node}' adicionado com sucesso!")
        
        elif opcao == "Remover node":
            nodes_removiveis: List[str] = [n for n in grafo.nodes if n != "Centro de Distribuição"]
            if not nodes_removiveis:
                print("Não há nodes para remover.")
                continue
            node: str = questionary.select("Escolha o node a remover:", choices=nodes_removiveis).ask()
            grafo.remover_node(node)
            print(f"Node '{node}' removido com sucesso!")
        
        elif opcao == "Editar node":
            nodes_editaveis: List[str] = [n for n in grafo.nodes if n != "Centro de Distribuição"]
            if not nodes_editaveis:
                print("Não há nodes para editar.")
                continue
            node_antigo: str = questionary.select("Escolha o node a editar:", choices=nodes_editaveis).ask()
            node_novo: str = questionary.text("Novo nome do node:").ask()
            grafo.editar_node(node_antigo, node_novo)
            print(f"Node '{node_antigo}' alterado para '{node_novo}'!")
        
        elif opcao == "Adicionar ligação":
            if len(grafo.nodes) < 2:
                print("É necessário pelo menos dois nodes para adicionar uma ligação.")
                continue
            node1: str = questionary.select("Escolha o primeiro node:", choices=list(grafo.nodes)).ask()
            node2: str = questionary.select("Escolha o segundo node:", choices=list(grafo.nodes)).ask()
            if node1 == node2:
                print("Os nodes devem ser diferentes.")
                continue
            distancia: str = questionary.text("Distância (km):").ask()
            try:
                distancia_float: float = float(distancia)
                grafo.adicionar_ligacao(node1, node2, distancia_float)
                print(f"Ligação entre '{node1}' e '{node2}' adicionada com distância {distancia_float} km!")
            except ValueError:
                print("Distância inválida. Deve ser um número.")
        
        elif opcao == "Adicionar pedido":
            if not grafo.nodes:
                print("Não há nodes para associar pedidos.")
                continue
            produto: str = questionary.text("Nome do produto:").ask()
            node: str = questionary.select("Escolha o node de entrega:", choices=list(grafo.nodes)).ask()
            pedidos.adicionar_pedido(produto, node)
            print(f"Pedido de '{produto}' para '{node}' adicionado!")
        
        elif opcao == "Remover pedido":
            if not pedidos.pedidos:
                print("Não há pedidos para remover.")
                continue
            produto: str = questionary.select("Escolha o pedido a remover:", choices=list(pedidos.pedidos.keys())).ask()
            pedidos.remover_pedido(produto)
            print(f"Pedido de '{produto}' removido!")
        
        elif opcao == "Listar pedidos":
            pedidos.listar_pedidos()
        
        elif opcao == "Calcular rota e gerar relatório":
            if not pedidos.pedidos:
                print("Não há pedidos para entregar.")
                continue
            rota: List[Tuple[str, str, float]]
            distancia_total: float
            rota, distancia_total = calcular_rota(grafo, pedidos.pedidos)
            gerar_relatorio(rota, distancia_total, pedidos.pedidos)
        
        elif opcao == "Sair":
            print("Saindo...")
            break

if __name__ == '__main__':
    menu()