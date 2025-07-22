# Sistema de Gerenciamento de Empréstimos

Desafio, desenvolver uma API REST que permita usuários gerenciar empréstimos..

## Configuração do Docker

O projeto está configurado para rodar em contêineres Docker para desenvolvimento.

### Pré-requisitos

- Docker instalado
- Docker Compose instalado


## 🚀 Funcionalidades

- Autenticação e autorização de usuários
- Criação e gerenciamento de empréstimos
- Processamento de pagamentos
- Cálculos de saldo
- Endpoints da API REST

## 🛠️ Tecnologias

- Django 🐍
- Python 3.12
- Docker 🐳
- PostgreSQL 🐘
- OpenWeather API ☁️
- Django REST Framework


## 🗂️ Estrutura do Projeto
    
        ├── Dockerfile
    ├── emprestimo
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── 0002_pagamento.py
    │   │   ├── 0003_alter_emprestimo_data_solicitacao.py
    │   │   └── __init__.py
    │   ├── models
    │   │   ├── emprestimo.py
    │   │   ├── __init__.py
    │   │   └── pagamento.py
    │   ├── serializers
    │   │   ├── emprestimo.py
    │   │   ├── __init__.py
    │   │   └── pagamento.py
    │   ├── test
    │   │   ├── base
    │   │   │   └── base_api_test_case.py
    │   │   ├── __init__.py
    │   │   ├── models
    │   │   │   ├── test_model_emprestimo.py
    │   │   │   └── test_model_pagamento.py
    │   │   └── views
    │   │       ├── __init__.py
    │   │       ├── test_emprestimo.py
    │   │       └── test_pagamento.py
    │   ├── urls.py
    │   └── views
    │       ├── emprestimo.py
    │       ├── __init__.py
    │       └── pagamento.py
    ├── gerenciador_emprestimo
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── infra
    │   ├── docker-compose.yml
    │   └── run.sh
    ├── manage.py
    ├── README.md
    ├── requirements.txt
    ├── static
    └── vagas
        └── README.md

## ⚙️ Configuração e Execução


1. Clone o repositório:

```
    git clone git@github.com:reginaldo-castro/desafio.git
    cd infra/
```

## 🗒️ 2. Criar o arquivo `.env`

Remover o `_exemplo` do `.env` na pasta `infra/` do projeto com o seguinte conteúdo:

```env
POSTGRES_DB=db_gerenciador
POSTGRES_USER=postgres
POSTGRES_PASSWORD=gerenciadoremprestimos
DB_HOST=db
DB_PORT=5432
```

## 🐳 3. Subir os containers
```
docker-compose up --build
```
## 📚 Documentação da API

A documentação da API REST está disponível nos formatos interativos abaixo:

- Swagger UI: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- OpenAPI(JSON): [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)
  

## 🐘 Acesso ao banco PostgreSQL (opcional)

- Host: db
- Porta: 5432
- Usuário: postgres
- Senha: gerenciadoremprestimos
- Banco: db_gerenciador

## 📋 Testes Automatizados

```
O projeto conta com uma suíte de testes automatizados utilizando o framework de testes do Django. 
Eles garantem a confiabilidade das funcionalidades da API e dos modelos.
```

### Como executar os testes

docker-compose exec infra-web-1 python manage.py test
  
### Organização dos testes

- emprestimo/test/models/ — testes unitários dos modelos (Emprestimo, Pagamento)
- emprestimo/test/views/ — testes de integração dos endpoints da API (emprestimos e pagamentos)
- emprestimo/test/base/ — casos base para os testes

## Testes implementados

#### Modelos
- Testes de criação, validação e relacionamento dos modelos Emprestimo e Pagamento.

### Views (API)
- Testes dos principais endpoints REST:

- GET /api/emprestimos/ — listar empréstimos
- POST /api/emprestimos/ — criar empréstimos
- GET /api/emprestimos/<uuid>/saldo_devedor/ — consulta de saldo devedor
- GET /api/emprestimos/resumo_financeiro/ — resumo financeiro
- GET /api/pagamentos/ — listar pagamentos
- POST /api/pagamentos/ — criar pagamentos

## 🗑️ Parar os containers
```
docker-compose down
```











 





