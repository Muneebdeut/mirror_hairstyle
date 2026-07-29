from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.api.routes_face import router as face_router
from app.api.routes_recommendations import router as rec_router
from app.api.routes_tryon import router as tryon_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.main")

app = FastAPI(
    title="AI Hairstyle Advisor API",
    description="Backend API for Face Detection, Facial Landmark Analysis, Face Shape Estimation, Hairstyle Recommendations, and AI Virtual Try-On.",
    version="1.0.0"
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production should restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Route Routers
app.include_router(face_router)
app.include_router(rec_router)
app.include_router(tryon_router)


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "service": "AI Hairstyle Advisor API",
        "version": "1.0.0"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception caught on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred. Please try again later.",
            "code": "INTERNAL_SERVER_ERROR"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
