from fastapi import FastAPI
from api.routes.resume_routes import router as resume_router

app = FastAPI(title="AI Resume Matcher")

# Register resume API routes
app.include_router(resume_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "AI Resume Matcher API is running"}
