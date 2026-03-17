# 🚀 Projeto: DimDim API (Containers)
API desenvolvida com FastAPI para gerenciamento de usuários e transações financeiras, utilizando Docker e integração com MySQL.

## Tecnologias
- Python
- FastAPI
- MySQL
- Docker
- Azure Container Registry
- Azure Container Instances

## Endpoints

### Users
POST /users
GET /users
PUT /users/{id}
DELETE /users/{id}

### Transactions
POST /transactions
GET /transactions
PUT /transactions/{id}
DELETE /transactions/{id}

## Banco de Dados

Tabelas:
- users
- transactions

# DimDim API

## Como rodar

1. Construir e subir containers:
```bash
docker-compose build
docker-compose up -d
# DimDim API

Acesse a API no http://localhost:8000 ou pelo endpoint público na Azure.

Endpoints disponíveis:

/users → CRUD de usuários
/transactions → CRUD de transações

2. Verificar o container do banco MySQL:
```bash
docker exec -it dimdim-db bash
docker exec -it dimdim-db bash
# senha: root
mysql -u root -p

### 📄 DDL das tabelas

```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100)
);

CREATE TABLE transactions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  amount DECIMAL(10,2),
  type VARCHAR(20),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
