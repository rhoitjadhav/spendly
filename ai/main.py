from fastapi import FastAPI
from gatekeeper.routers import router as gatekeeper_router

app = FastAPI(title="Agents", version="1.0.0")

app.include_router(gatekeeper_router)

if __name__ == '__main__':
    pass
