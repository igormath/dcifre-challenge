from fastapi import FastAPI
from router_empresa import router_empresa

app = FastAPI()

app.include_router(router=router_empresa)
