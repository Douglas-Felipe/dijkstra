# Sistema de Roteamento de Entregas

Este projeto implementa um sistema para calcular rotas de entrega otimizadas com base em um grafo de localizações e uma lista de pedidos. Ele utiliza o algoritmo de Dijkstra para encontrar os caminhos mais curtos e uma heurística de vizinho mais próximo para determinar a ordem de visita aos pontos de entrega. O sistema oferece uma interface de linha de comando (CLI) interativa para gerenciar o grafo, os pedidos e calcular as rotas.

## Índice
- [Funcionalidades Principais](#funcionalidades-principais)
- [Estrutura dos Arquivos](#estrutura-dos-arquivos)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)

## Funcionalidades Principais

*   **Gerenciamento de Grafo:**
    *   Adicionar, remover e editar nós (localizações) no grafo.
    *   Adicionar ligações (arestas) entre nós com distâncias especificadas.
    *   O nó "Centro de Distribuição" é fixo e serve como ponto de partida/retorno.
*   **Gerenciamento de Pedidos:**
    *   Adicionar pedidos associando um produto a um nó de destino.
    *   Remover pedidos existentes.
    *   Listar todos os pedidos atuais.
*   **Cálculo de Rota:**
    *   Calcula a rota mais curta partindo do "Centro de Distribuição", visitando todos os nós com pedidos pendentes e retornando (implicitamente, ao terminar no último nó de entrega).
    *   Utiliza o algoritmo de Dijkstra para encontrar o caminho mais curto entre dois pontos.
    *   Emprega uma heurística de vizinho mais próximo para decidir qual o próximo nó de entrega a visitar.
*   **Geração de Relatório:**
    *   Exibe um relatório detalhado da rota calculada, incluindo cada trecho (origem, destino, distância) e a distância total percorrida.
    *   Indica quais trechos correspondem à entrega de um pedido específico.
*   **Visualização do Grafo:**
    *   Gera uma representação visual do grafo de nós e ligações usando `networkx` e `matplotlib`. O "Centro de Distribuição" é destacado.
*   **Persistência de Dados:**
    *   **Cache JSON:** Salva e carrega automaticamente o estado atual do grafo (`grafo.json`) e dos pedidos (`pedidos.json`) ao sair e iniciar o programa, respectivamente.
    *   **Banco de Dados Oracle:** Permite salvar o estado atual do grafo e dos pedidos com um nome específico no banco de dados Oracle e carregar estados salvos anteriormente.

## Estrutura dos Arquivos

*   **`main.py`**:
    *   Ponto de entrada principal da aplicação.
    *   Contém o loop principal e a lógica do menu interativo usando `questionary`.
    *   Orquestra as chamadas para as funcionalidades definidas nos outros módulos.
    *   Gerencia a conexão com o banco de dados e o carregamento/salvamento inicial/final do cache JSON.
*   **`grafo.py`**:
    *   Define a classe `Grafo`.
    *   Implementa métodos para adicionar, remover e editar nós e ligações.
    *   Contém a lógica para exibir o grafo visualmente (`exibir_grafo`).
    *   Implementa a funcionalidade de salvar e carregar o grafo em formato JSON (`salvar_json`, `carregar_json`).
*   **`pedidos.py`**:
    *   Define a classe `Pedidos`.
    *   Implementa métodos para adicionar, remover e listar pedidos.
    *   Implementa a funcionalidade de salvar e carregar os pedidos em formato JSON (`salvar_json`, `carregar_json`).
*   **`rota.py`**:
    *   Contém a implementação do algoritmo de Dijkstra (`dijkstra`) para encontrar o caminho mais curto entre um nó de origem e todos os outros nós no grafo.
    *   Define a função `calcular_rota` que utiliza Dijkstra e a heurística do vizinho mais próximo para determinar a sequência de visita aos nós de entrega e o caminho completo.
*   **`relatorio.py`**:
    *   Define a função `gerar_relatorio` que formata e imprime o relatório da rota calculada, incluindo detalhes de entrega e distância total.
*   **`database.py`**:
    *   Define a classe `Database` para interagir com o banco de dados Oracle.
    *   Gerencia a conexão e desconexão.
    *   Contém métodos para criar as tabelas necessárias (se não existirem).
    *   Implementa a lógica para salvar (`salvar_grafo`) e carregar (`carregar_grafo`) o estado do grafo e dos pedidos do/para o banco de dados.
    *   Utiliza variáveis de ambiente (via `.env`) para as credenciais do banco de dados.
*   **`.env` (Não incluído, deve ser criado)**:
    *   Arquivo para armazenar as credenciais do banco de dados Oracle de forma segura.
*   **`grafo.json` (Gerado)**:
    *   Arquivo de cache para o estado do grafo.
*   **`pedidos.json` (Gerado)**:
    *   Arquivo de cache para o estado dos pedidos.

## Pré-requisitos

*   Python 3.8 ou superior.
*   Oracle Database (instância acessível para a funcionalidade de banco de dados).
*   Oracle Instant Client (ou Oracle Client completo) configurado corretamente para a biblioteca `oracledb`.
*   Bibliotecas Python listadas em `requirements.txt`.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:Douglas-Felipe/dijkstra.git
    cd dijkstra
    ```
2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as variáveis de ambiente:**
    *   Crie um arquivo chamado `.env` na raiz do projeto.
    *   Adicione suas credenciais do Oracle Database neste arquivo. Veja o exemplo em `.env.example`.

## Configuração

*   **Banco de Dados:**
    *   Certifique-se de que o Oracle Instant Client esteja no PATH do sistema ou que suas variáveis de ambiente (`LD_LIBRARY_PATH` no Linux, `PATH` no Windows) apontem para ele.
    *   Preencha o arquivo `.env` com suas credenciais:
      ```dotenv
      # .env
      ORACLE_USER=seu_usuario_oracle
      ORACLE_PASSWORD=sua_senha_oracle
      ORACLE_DSN=seu_dsn_oracle (ex: localhost:1521/XEPDB1)
      ```
    *   Na primeira execução *se* for usar o banco de dados, pode ser necessário descomentar a linha `db.criar_tabelas()` em `main.py` para criar as tabelas no seu schema Oracle. Após a criação, comente a linha novamente.
    * Caso queira também é possível popular o banco com grafos e pedidos pré prontos. Basta esecutar o arquivo `populate_db.sql` em seu banco de dados oracle

## Uso

1.  Execute o script principal:
    ```bash
    python main.py
    ```
2.  O programa iniciará e carregará os dados dos arquivos `grafo.json` e `pedidos.json`, se existirem.
3.  Use o menu interativo para escolher as ações desejadas:
    *   Adicionar/Remover/Editar Nós e Ligações para construir seu mapa de entregas.
    *   Adicionar/Remover/Listar Pedidos para definir os destinos.
    *   Calcular Rota e Gerar Relatório para ver a solução otimizada.
    *   Exibir Grafo para uma visualização gráfica.
    *   Salvar/Carregar do Banco de Dados para persistência de longo prazo.
4.  Ao escolher "Sair", o estado atual do grafo e dos pedidos será salvo nos arquivos JSON (`grafo.json`, `pedidos.json`).

