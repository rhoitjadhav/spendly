import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def run_app():
    from app.routers.export import router as export_router
    from app.routers.jobs import router as jobs_router
    from app.routers.lendings import router as lendings_router
    from app.routers.stats import router as stats_router
    from app.routers.transactions import router as transactions_router
    from app.routers.upload import router as upload_router

    app = FastAPI(title="Spendly", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(upload_router)
    app.include_router(jobs_router)
    app.include_router(transactions_router)
    app.include_router(stats_router)
    app.include_router(export_router)
    app.include_router(lendings_router)

    return app


def run_ai():
    from ai.routers import router as ai_router

    app = FastAPI(title="Agents", version="1.0.0")

    app.include_router(ai_router)

    return app


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ai":
        _app = run_ai()
        port = 8100
    else:
        _app = run_app()
        port = 8200

    uvicorn.run(_app, host="0.0.0.0", port=port)
