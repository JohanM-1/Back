from fastapi import FastAPI
from routers import userRouter  # Import the router object

app = FastAPI()

# Include the router in the app
app.include_router(userRouter.router)