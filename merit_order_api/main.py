import logging.config
import os
import uvicorn

from fastapi import FastAPI, status, Depends
from merit_order_api.dependencies import get_settings
from merit_order_api.v1_routes import api_router as v1


dir_name = os.path.dirname(__file__)
settings = get_settings()


def get_application():
    logging.config.fileConfig(f"{dir_name}/logging.ini", disable_existing_loggers=False)
    logging.basicConfig(level=logging.INFO)
    _app = FastAPI(title=get_settings().PROJECT_NAME, dependencies=[Depends(get_settings)])

    return _app


app = get_application()
app.include_router(v1.router,
                   dependencies=[Depends(get_settings)], tags=["powerplant-coding-challenge"])


@app.get("/_healthcheck", status_code=status.HTTP_200_OK)
def healthcheck():
    return {"status": "OK"}


@app.on_event("startup")
async def startup():
    logging.info("Startup")


@app.on_event("shutdown")
async def shutdown():
    logging.info("Shutdown")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
