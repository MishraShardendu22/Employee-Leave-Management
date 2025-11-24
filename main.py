from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/api/test")
def root():
    return {"message": "API is working"}

# 


if __name__ == "__main__":
    main()
