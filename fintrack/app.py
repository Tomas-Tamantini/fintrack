from fastapi import FastAPI

from fintrack.api.routes import all_routes

app = FastAPI()
for router in all_routes:
    app.include_router(router)
