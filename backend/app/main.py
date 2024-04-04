from fastapi import FastAPI
from routers import stats
import uvicorn

app = FastAPI()


app.include_router(stats.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)