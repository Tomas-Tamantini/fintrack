from fintrack.api.routes.authentication import auth_router
from fintrack.api.routes.user import users_router

all_routes = (auth_router, users_router)
