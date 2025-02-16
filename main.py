from fastapi import FastAPI
from routes_empresa import route_empresa
from routes_obrigacao_acessoria import route_obrigacao_acessoria

app = FastAPI()

app.include_router(router=route_empresa)
app.include_router(router=route_obrigacao_acessoria)
