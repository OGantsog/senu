import uvicorn
from fastapi import FastAPI, APIRouter

router = APIRouter(prefix="/items", tags=["items"])


@router.api_route("/")
async def items():
    return {"test": "items"}


app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "World World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
