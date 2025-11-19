from fastapi import FastAPI
from API.Routes.user_routes import router as user_router

app = FastAPI(
    title="User Service",
    description="Handles user registration, login, and role-based authentication.",
    version="1.0.0"
)

app.include_router(user_router, prefix="/user", tags=["User"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "User Service"}
