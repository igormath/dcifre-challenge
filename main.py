from fastapi import FastAPI
from router_empresa import router_empresa
from router_obrigacao_acessoria import router_obrigacao_acessoria

app = FastAPI()

app.include_router(router=router_empresa)
app.include_router(router=router_obrigacao_acessoria)
