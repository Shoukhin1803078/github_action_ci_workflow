from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello world! . CI/CD is completed. I love CI/CD deployment learning."}