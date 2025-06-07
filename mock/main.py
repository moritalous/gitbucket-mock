from fastapi import FastAPI

from routers import api_router

app = FastAPI(
    title="GitBucket Mock API",
    description="A mock implementation of GitBucket API using FastAPI",
    version="0.1.0",
)

# Register all API routers at once
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
