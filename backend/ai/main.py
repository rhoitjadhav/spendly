import uvicorn
from fastapi import FastAPI
from routers import router

app = FastAPI(title="Agents", version="1.0.0")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
