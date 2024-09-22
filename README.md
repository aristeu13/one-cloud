# OneCloud API

Este projeto fornece uma aplicação FastAPI integrada com MongoDB para gerenciar usuários e administradores, suportando autenticação baseada em JWT para validação de funções, e inclui testes usando pytest para testes unitários e de integração.

### Funcionalidades

- **FastAPI**: Fornece um framework rápido e escalável para construção de APIs.
- **MongoDB**: Armazena os dados de usuários e administradores.
- **Autenticação JWT**: Autenticação segura baseada em funções (usuários e administradores) com tokens JWT.
- **Integração Terceira**: implementação de chamadas para uma API externa para verificar o papel do usuário (usuário ou admin), obter informações dinâmicas e também o token.
- **Testes Unitários e de Integração**: Uso de pytest e httpx para testes extensivos.
- **Suporte a Docker**: O app roda em um container Docker com MongoDB, e há arquivos docker-compose separados para ambientes de desenvolvimento e testes.

### Pré-requisitos

Para rodar este projeto localmente, certifique-se de ter o seguinte instalado:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/)

## Configuração do Projeto
### Clonar o repositório

```bash
git clone https://github.com/aristeu13/one-cloud.git
cd one-cloud
```


### Executando a Aplicação com Docker (Recomendado)
#### 1. Usando Docker Compose

Para construir e rodar o app usando Docker, execute o seguinte comando:

```bash
docker-compose up --build
```

A API estará disponível em http://localhost:8000. Você também pode visualizar a documentação interativa da API em http://localhost:8000/docs.

#### 2. Executando os Testes
Testes Unitários e de Integração

Os testes de integração estão configurados para testar as APIs, o banco de dados e as respostas de serviços externos.

Para rodar todos os testes use o seguinte comando:

```bash
docker-compose -f docker-compose.test.yml up --build
```

# Estrutura do Projeto

```bash
.
├── app/
│   ├── api/               # Rotas da API
│   ├── core/              # Utilitários principais como DB e autenticação JWT
│   ├── application/       # Serviços, repositórios
│   └── main.py            # Ponto de entrada da aplicação
├── tests/                 # Testes unitários e de integração
├── docker-compose.yml     # Configuração do Docker para a aplicação
├── docker-compose.test.yml# Configuração do Docker para testes
├── requirements.txt       # Dependências para o Docker
├── README.md              # Documentação do projeto
└── pyproject.toml         # Dependências do Poetry
```