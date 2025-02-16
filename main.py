from fastapi import FastAPI
from routes_empresa import route_empresa
from routes_obrigacao_acessoria import route_obrigacao_acessoria

tags_metadata = [
    {"name": "Métodos Get Empresa", "description": "Métodos para recuperar informações de Empresas salvas no banco."},
    {"name": "Métodos Get Obrigação Acessória", "description": "Métodos para recuperar informações de Obrigações Acessórias salvas no banco."},
    {"name": "Método Post Empresa", "description": "Método para adicionar nova Empresa ao banco de dados."},
    {"name": "Método Post Obrigação Acessória", "description": "Método para adicionar nova Obrigação Acessória ao banco de dados."},
    {"name": "Método Delete Empresa", "description": "Método para remover Empresa do banco de dados."},
    {"name": "Método Delete Obrigação Acessória", "description": "Método para remover Obrigação Acessória do banco de dados."},
    {"name": "Método Put Empresa", "description": "Método para atualizar informações da Empresa salva no banco de dados."},
    {"name": "Método Put Obrigação Acessória", "description": "Método para atualizar informações da Obrigação Acessória salva no banco de dados."},
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(router=route_empresa)
app.include_router(router=route_obrigacao_acessoria)
