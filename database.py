from grafo import Grafo
import oracledb
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
import os

from pedidos import Pedidos

# Carrega as variáveis do arquivo .env
load_dotenv()

class Database:
    def __init__(self) -> None:
        self.user: str = os.getenv("ORACLE_USER")
        self.password: str = os.getenv("ORACLE_PASSWORD")
        self.dsn: str = os.getenv("ORACLE_DSN")
        self.conn: Optional[oracledb.Connection] = None
        self.cursor: Optional[oracledb.Cursor] = None

        # Verifica se as credenciais foram carregadas corretamente
        if not all([self.user, self.password, self.dsn]):
            raise ValueError("Credenciais do Oracle não encontradas no arquivo .env")

    def conectar(self) -> None:
        try:
            self.conn = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)
            self.cursor = self.conn.cursor()
            print("Conectado ao banco de dados Oracle com sucesso!")
        except oracledb.Error as e:
            print(f"Erro ao conectar ao banco: {e}")

    def desconectar(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Desconectado do banco de dados.")

    def criar_tabelas(self) -> None:
        try:
            self.cursor.execute("""
                CREATE TABLE grafos (
                    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nome VARCHAR2(100) UNIQUE NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE nodes (
                    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    grafo_id NUMBER NOT NULL,
                    nome VARCHAR2(100) NOT NULL,
                    FOREIGN KEY (grafo_id) REFERENCES grafos(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE ligacoes (
                    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    grafo_id NUMBER NOT NULL,
                    node1 VARCHAR2(100) NOT NULL,
                    node2 VARCHAR2(100) NOT NULL,
                    distancia NUMBER NOT NULL,
                    FOREIGN KEY (grafo_id) REFERENCES grafos(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE pedidos (
                    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    grafo_id NUMBER NOT NULL,
                    produto VARCHAR2(100) NOT NULL,
                    node VARCHAR2(100) NOT NULL,
                    FOREIGN KEY (grafo_id) REFERENCES grafos(id)
                )
            """)
            self.conn.commit()
            print("Tabelas criadas com sucesso!")
        except oracledb.Error as e:
            print(f"Erro ao criar tabelas: {e}")
            self.conn.rollback()

    def salvar_grafo(self, nome_grafo: str, grafo: Grafo, pedidos: Pedidos) -> None:
        try:
            self.cursor.execute("INSERT INTO grafos (nome) VALUES (:1) RETURNING id INTO :2", (nome_grafo, 0))
            grafo_id = self.cursor.var(oracledb.NUMBER).getvalue()[0]
            
            for node in grafo.nodes:
                self.cursor.execute("INSERT INTO nodes (grafo_id, nome) VALUES (:1, :2)", (grafo_id, node))

            exibidos = set()
            for node in grafo.nodes:
                for vizinho, distancia in grafo.ligacoes[node].items():
                    par = tuple(sorted([node, vizinho]))
                    if par not in exibidos:
                        exibidos.add(par)
                        self.cursor.execute(
                            "INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (:1, :2, :3, :4)",
                            (grafo_id, node, vizinho, distancia)
                        )

            for produto, node in pedidos.pedidos.items():
                self.cursor.execute(
                    "INSERT INTO pedidos (grafo_id, produto, node) VALUES (:1, :2, :3)",
                    (grafo_id, produto, node)
                )

            self.conn.commit()
            print(f"Grafo '{nome_grafo}' salvo no banco de dados!")
        except oracledb.Error as e:
            print(f"Erro ao salvar o grafo: {e}")
            self.conn.rollback()

    def listar_grafos(self) -> List[str]:
        try:
            self.cursor.execute("SELECT nome FROM grafos")
            return [row[0] for row in self.cursor.fetchall()]
        except oracledb.Error as e:
            print(f"Erro ao listar grafos: {e}")
            return []

    def carregar_grafo(self, nome_grafo: str, grafo: Grafo, pedidos: Pedidos) -> None:
        try:
            self.cursor.execute("SELECT id FROM grafos WHERE nome = :1", (nome_grafo,))
            result = self.cursor.fetchone()
            if not result:
                print(f"Grafo '{nome_grafo}' não encontrado.")
                return
            grafo_id = result[0]

            grafo.nodes.clear()
            grafo.ligacoes.clear()
            self.cursor.execute("SELECT nome FROM nodes WHERE grafo_id = :1", (grafo_id,))
            for row in self.cursor.fetchall():
                grafo.adicionar_node(row[0])

            self.cursor.execute("SELECT node1, node2, distancia FROM ligacoes WHERE grafo_id = :1", (grafo_id,))
            for node1, node2, distancia in self.cursor.fetchall():
                grafo.adicionar_ligacao(node1, node2, distancia)

            pedidos.pedidos.clear()
            self.cursor.execute("SELECT produto, node FROM pedidos WHERE grafo_id = :1", (grafo_id,))
            for produto, node in self.cursor.fetchall():
                pedidos.adicionar_pedido(produto, node)

            print(f"Grafo '{nome_grafo}' carregado do banco de dados!")
        except oracledb.Error as e:
            print(f"Erro ao carregar o grafo: {e}")