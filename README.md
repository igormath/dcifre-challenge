# Dcifre Challenge

## Objetivo

Criar uma API simples utilizando FastAPI, Pydantic, SQLAlchemy para cadastrar
empresas e gerenciar obrigações acessórias que a empresa precisa declarar para o
governo.

## Como rodar a aplicação:
A API foi desenvolvida na versão 3.13.1 do Python, que pode ser obtida [aqui](https://www.python.org/downloads/).

### Passo a passo:
1) Clone ou faça download deste repositório:

```bash
git clone git@github.com:igormath/dcifre-challenge.git
```
2) [Crie e ative um ambiente virtual](https://dev.to/franciscojdsjr/guia-completo-para-usar-o-virtual-environment-venv-no-python-57bo) na pasta em que o projeto foi baixado.

3) Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

4) Renomeie o arquivo **.env-example** para **.env**, e substitua os campos **{USERNAME}**, **{PASSWORD}** e **{DATABASE_NAME}** pelos seus respectivos dados do banco de dados [Postgres](https://www.postgresql.org/download/).

5) Inicie a aplicação:
```bash
fastapi dev main.py
```

## Swagger API
- [Rotas e Schemas utilizadas](https://drive.google.com/file/d/1F_cIDW0afllw5zg7NClyIZM4gcvm6VrL/view) - Aguarde a imagem carregar para dar zoom.

## Referências utilizadas:
- [Using migrations in Python — SQLAlchemy with Alembic + Docker solution](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)
- [Tutorial - Alembic 1.14.1 documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#project-structure)
- [Como criar uma API REST usando Python com FastAPI Framework](https://medium.com/@vinicius_/como-criar-uma-api-rest-usando-python-com-fastapi-framework-1701849c0ce6)
- [Import APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/#import-apirouter)
- [How to group FastAPI endpoints in Swagger UI?](https://stackoverflow.com/questions/63762387/how-to-group-fastapi-endpoints-in-swagger-ui)
