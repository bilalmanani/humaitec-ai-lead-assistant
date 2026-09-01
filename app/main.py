from fastapi import FastAPI



app=FastAPI(title="HUMAITEC AI Lead & Knowledge Assistant")


@app.get("/")
def home():
    return {"message":"Humaitec AI lead & knowledge assistant is runing"}


@app.get("/health")
def health():
    return{
        "status":"healthy"
    }