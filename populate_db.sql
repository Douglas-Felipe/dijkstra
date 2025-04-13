-- Limpar tabelas existentes (opcional, para evitar erros se as tabelas já existirem)
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE pedidos CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE ligacoes CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE nodes CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE grafos CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN -- Ignora erro "tabela não existe"
         RAISE;
      END IF;
END;
/

-- Criar tabela para grafos
CREATE TABLE grafos (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100) UNIQUE NOT NULL
);

-- Criar tabela para nodes
CREATE TABLE nodes (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    grafo_id NUMBER NOT NULL,
    nome VARCHAR2(100) NOT NULL,
    FOREIGN KEY (grafo_id) REFERENCES grafos(id)
);

-- Criar tabela para ligações (arestas)
CREATE TABLE ligacoes (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    grafo_id NUMBER NOT NULL,
    node1 VARCHAR2(100) NOT NULL,
    node2 VARCHAR2(100) NOT NULL,
    distancia NUMBER NOT NULL,
    FOREIGN KEY (grafo_id) REFERENCES grafos(id)
);

-- Criar tabela para pedidos
CREATE TABLE pedidos (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    grafo_id NUMBER NOT NULL,
    produto VARCHAR2(100) NOT NULL,
    node VARCHAR2(100) NOT NULL,
    FOREIGN KEY (grafo_id) REFERENCES grafos(id)
);

-- Bloco PL/SQL para inserir os dados
BEGIN
    -- Declaração de variáveis
    DECLARE
        grafo_urbano_id NUMBER;
        grafo_rural_id NUMBER;
    BEGIN
        -- Inserir o primeiro grafo: "Grafo Urbano"
        INSERT INTO grafos (nome) VALUES ('Grafo Urbano')
        RETURNING id INTO grafo_urbano_id;

        -- Inserir nodes do Grafo Urbano
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_urbano_id, 'Centro de Distribuição');
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_urbano_id, 'A');
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_urbano_id, 'B');
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_urbano_id, 'C');
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_urbano_id, 'D');

        -- Inserir ligações do Grafo Urbano
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_urbano_id, 'Centro de Distribuição', 'A', 5);
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_urbano_id, 'Centro de Distribuição', 'B', 2);
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_urbano_id, 'A', 'C', 3);
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_urbano_id, 'B', 'C', 3);
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_urbano_id, 'C', 'D', 1);

        -- Inserir pedidos do Grafo Urbano
        INSERT INTO pedidos (grafo_id, produto, node) VALUES (grafo_urbano_id, 'Agente X', 'C');
        INSERT INTO pedidos (grafo_id, produto, node) VALUES (grafo_urbano_id, 'NPK', 'D');

        -- Inserir o segundo grafo: "Grafo Rural"
        INSERT INTO grafos (nome) VALUES ('Grafo Rural')
        RETURNING id INTO grafo_rural_id;

        -- Inserir nodes do Grafo Rural
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_rural_id, 'Centro de Distribuição');
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_rural_id, 'Fazenda 1');
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_rural_id, 'Fazenda 2');
        INSERT INTO nodes (grafo_id, nome) VALUES (grafo_rural_id, 'Fazenda 3');

        -- Inserir ligações do Grafo Rural
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_rural_id, 'Centro de Distribuição', 'Fazenda 1', 10);
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_rural_id, 'Centro de Distribuição', 'Fazenda 2', 15);
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_rural_id, 'Fazenda 1', 'Fazenda 3', 7);
        INSERT INTO ligacoes (grafo_id, node1, node2, distancia) VALUES (grafo_rural_id, 'Fazenda 2', 'Fazenda 3', 5);

        -- Inserir pedidos do Grafo Rural
        INSERT INTO pedidos (grafo_id, produto, node) VALUES (grafo_rural_id, 'Fertilizante A', 'Fazenda 1');
        INSERT INTO pedidos (grafo_id, produto, node) VALUES (grafo_rural_id, 'Sementes B', 'Fazenda 3');

        -- Confirmar as inserções
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Erro ao inserir dados: ' || SQLERRM);
            ROLLBACK;
            RAISE;
    END;
END;
/

-- Consultas para verificar os dados (opcional)
SELECT * FROM grafos;
SELECT * FROM nodes;
SELECT * FROM ligacoes;
SELECT * FROM pedidos;