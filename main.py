import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any

from database import db, create_document, get_documents

app = FastAPI(title="SiMATA - Sistem Informasi Manajemen Aset & Tata Kelola")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateRequest(BaseModel):
    collection: str
    data: dict


@app.get("/")
def read_root():
    return {"name": "SiMATA", "version": "0.1", "message": "Backend berjalan"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


@app.get("/api/collections")
def list_collections():
    try:
        cols = db.list_collection_names() if db else []
        return {"collections": cols}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/create")
def create_generic(payload: CreateRequest):
    try:
        inserted_id = create_document(payload.collection, payload.data)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/list/{collection}")
def list_generic(collection: str, limit: Optional[int] = 50):
    try:
        docs = get_documents(collection, limit=limit)
        # Convert ObjectId to string if present
        result: List[Any] = []
        for d in docs:
            d = dict(d)
            if "_id" in d:
                d["_id"] = str(d["_id"])
            result.append(d)
        return {"items": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
