from fastapi import FastAPI
from routers import user_router,snake_router  # Import the router object
app = FastAPI()

# Include the router in the app
app.include_router(user_router.router)
app.include_router(snake_router.router)