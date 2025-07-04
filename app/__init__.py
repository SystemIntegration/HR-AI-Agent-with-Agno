from fastapi import FastAPI
from app.routes.routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.configurations.logger import logger


def create_app():

    app = FastAPI()

    app.mount("/assets", StaticFiles(directory="./frontend/dist/assets"), name="assets")
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

    # Middleware example with the shared logger
    @app.middleware("http")
    async def log_requests(request, call_next):
        # logger.info(f"Request: {request.method} {request.url}")
        try:
            response = await call_next(request)
            # logger.info(f"Response: {response.status_code}")
            return response
        except Exception:
            logger.exception("Unhandled Exception occurred")
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
        
    # Register your routes with the app
    app.include_router(router)

    return app
