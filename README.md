# MADR - Meu acervo digital de romances

API REST para gerenciamento de um acervo digital de romances, permitindo o controle de contas de usuários, cadastro de livros e gerenciamento de romancistas.

## Tecnologias utilizadas
- Python 3.12
- FastAPI
- SQLAlchemy 
- PostgreSQL
- Alembic
- Pytest
- Poetry
- Docker e Docker Compose

## Funcionalidades

### Contas
- Criar conta  
- Atualizar conta  
- Deletar conta  
- Login e geração de token JWT  
- Refresh de token  

### Livros
- Criar livro  
- Atualizar livro  
- Deletar livro  
- Buscar por ID  
- Buscar por filtros (título e ano) com paginação  

### Romancistas
- Criar romancista  
- Atualizar romancista  
- Deletar romancista  
- Buscar por ID  
- Buscar por nome parcial com paginação  

## Como usar a API

### Autenticação (FastAPI Users)

- Registrar usuário: `POST /auth/register`  
- Login: `POST /auth/jwt/login`  
- Logout: `POST /auth/jwt/logout`  
- Refresh token: `POST /auth/jwt/refresh`  

### Fluxo básico

1. Registre um usuário  
2. Faça login e obtenha o token JWT  
3. Envie o token no header das requisições:

```
Authorization: Bearer <token>
```

4. Gerencie romancistas: `POST /authors`, `PATCH /books/{id}`, `DELETE /authors/{id}`  
5. Gerencie livros: `POST /books`, `PATCH /books/{id}`, `DELETE /books/{id}`  

Documentação interativa disponível em:

```
http://localhost:8000/docs
```
## Usando o projeto

Caso queira contribuir, estudar ou adaptar o projeto:

1. Faça um fork do repositório  
2. Clone o fork:

```
git clone https://github.com/seu-usuario/madr.git
cd madr
```

3. Crie uma branch:

```
git checkout -b minha-feature
```

4. Instale as dependências:

```bash
poetry install
```

5. Suba o ambiente:

```
docker compose up --build
```

6. Após finalizar, execute os testes:

```
poetry run pytest ou task test (com taskpy)
```

7. Faça commit e push:

```
git add .
git commit -m "feat: minha feature"
git push origin minha-feature
```

8. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.  
Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
