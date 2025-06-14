from fastapi import FastAPI

from fintrack.api.routes.user import users_router

app = FastAPI()


app.include_router(users_router)
