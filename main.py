import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Provider, Service, ServiceRequest, Review

app = FastAPI(title="Garden Services API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Garden Services API running"}


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
            response["database_name"] = getattr(db, "name", None) or "✅ Connected"
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

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# ---- Providers ----
@app.post("/providers", status_code=201)
def create_provider(provider: Provider):
    provider_id = create_document("provider", provider)
    return {"id": provider_id}


@app.get("/providers")
def list_providers():
    items = get_documents("provider")
    for i in items:
        i["id"] = str(i.pop("_id"))
    return items


# ---- Services ----
@app.post("/services", status_code=201)
def create_service(service: Service):
    service_id = create_document("service", service)
    return {"id": service_id}


@app.get("/services")
def list_services():
    items = get_documents("service")
    for i in items:
        i["id"] = str(i.pop("_id"))
    return items


# ---- Service Requests (client requests a service) ----
@app.post("/requests", status_code=201)
def create_request(req: ServiceRequest):
    request_id = create_document("servicerequest", req)
    return {"id": request_id}


@app.get("/requests")
def list_requests(status: Optional[str] = None):
    filt = {"status": status} if status else None
    items = get_documents("servicerequest", filt)
    for i in items:
        i["id"] = str(i.pop("_id"))
    return items


# ---- Reviews ----
@app.post("/reviews", status_code=201)
def create_review(review: Review):
    review_id = create_document("review", review)
    return {"id": review_id}


@app.get("/reviews")
def list_reviews(provider_id: Optional[str] = None):
    filt = {"provider_id": provider_id} if provider_id else None
    items = get_documents("review", filt)
    for i in items:
        i["id"] = str(i.pop("_id"))
    return items


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
