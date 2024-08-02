import uvicorn
from app.api.v1.routers import app


if __name__ == '__main__':
    uvicorn.run(app, port=8000, workers=2, log_level="info", reload=True)
