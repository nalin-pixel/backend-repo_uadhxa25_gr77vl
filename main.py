from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from database import db, create_document, get_documents

app = FastAPI(title="VDRONE API", description="CMS endpoints for VDRONE site", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Schemas
# ------------------------
class SiteContent(BaseModel):
    brand: str = "VDRONE"
    colors: Dict[str, str] = {
        "primary": "#00C2FF",
        "bg": "#0A0F19",
        "text": "#FFFFFF",
        "black": "#000000"
    }
    hero_title: str = "VDRONE – Explore the world from above"
    hero_cta: str = "Explorează Portofoliul"
    about_paragraphs: List[str] = [
        "Filmări aeriene spectaculoase la rezoluții 4K/8K.",
        "Fotografie profesională pentru imobiliare, evenimente și branduri.",
        "Inspecții industriale, cartografiere și producție corporate."
    ]

class ServiceItem(BaseModel):
    title: str
    description: str
    icon: str

class PortfolioItem(BaseModel):
    media_type: str  # image|video
    url: str
    thumbnail: Optional[str] = None
    category: str
    title: Optional[str] = None
    description: Optional[str] = None

class VideoItem(BaseModel):
    title: str
    url: str
    thumbnail: Optional[str] = None

class PhotoItem(BaseModel):
    title: Optional[str] = None
    url: str

class ContactMessage(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str

# ------------------------
# Seed default content if empty
# ------------------------
@app.on_event("startup")
def seed_defaults():
    try:
        # Site content
        if db is not None and db["sitecontent"].count_documents({}) == 0:
            default_content = SiteContent().model_dump()
            create_document("sitecontent", default_content)
        # Services
        if db is not None and db["serviceitem"].count_documents({}) == 0:
            defaults = [
                {"title": "Filmări aeriene 4K/8K", "description": "Cadre fluide, cinematice, la calitate maximă.", "icon": "Video"},
                {"title": "Fotografie aeriană profesională", "description": "Compoziții curate, perspective unice.", "icon": "Camera"},
                {"title": "Inspecții industriale", "description": "Evaluări rapide și sigure pentru zone greu accesibile.", "icon": "Shield"},
                {"title": "Filmări corporate & reclame", "description": "Spoturi dinamice pentru campanii memorabile.", "icon": "Briefcase"},
                {"title": "Cartografiere / mapping", "description": "Hărți precise și modele 3D.", "icon": "Map"},
                {"title": "Evenimente & nunți", "description": "Momente unice surprinse din aer.", "icon": "Heart"},
            ]
            for s in defaults:
                create_document("serviceitem", s)
        # Portfolio placeholders
        if db is not None and db["portfolioitem"].count_documents({}) == 0:
            placeholders = [
                {"media_type": "image", "url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop", "category": "Landscape", "title": "Mountain Range"},
                {"media_type": "image", "url": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?q=80&w=1600&auto=format&fit=crop", "category": "Real Estate", "title": "Modern Villa"},
                {"media_type": "video", "url": "https://videos.pexels.com/video-files/855331/855331-hd_1920_1080_25fps.mp4", "category": "Events", "title": "Outdoor Festival"},
                {"media_type": "image", "url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=1600&auto=format&fit=crop", "category": "Cinematic Shots", "title": "City Nights"},
                {"media_type": "image", "url": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1600&auto=format&fit=crop", "category": "Corporate", "title": "Business District"},
            ]
            for p in placeholders:
                create_document("portfolioitem", p)
        # Video gallery
        if db is not None and db["videoitem"].count_documents({}) == 0:
            vids = [
                {"title": "Showreel 2024", "url": "https://videos.pexels.com/video-files/855331/855331-hd_1920_1080_25fps.mp4"},
                {"title": "Real Estate Highlights", "url": "https://videos.pexels.com/video-files/857195/857195-hd_1920_1080_30fps.mp4"},
            ]
            for v in vids:
                create_document("videoitem", v)
        # Photo gallery
        if db is not None and db["photoitem"].count_documents({}) == 0:
            photos = [
                {"title": "Cliffs", "url": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1600&auto=format&fit=crop"},
                {"title": "City", "url": "https://images.unsplash.com/photo-1494526585095-c41746248156?q=80&w=1600&auto=format&fit=crop"},
                {"title": "Forest", "url": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1600&auto=format&fit=crop"},
            ]
            for ph in photos:
                create_document("photoitem", ph)
    except Exception:
        # In case DB not configured, skip seeding silently
        pass

# ------------------------
# Public endpoints
# ------------------------
@app.get("/test")
def test():
    # Validate DB connectivity if available
    ok = db is not None
    return {"ok": True, "db": ok}

@app.get("/content")
def get_content():
    docs = get_documents("sitecontent", {}) if db else []
    if docs:
        d = docs[-1]
        d["_id"] = str(d.get("_id"))
        return d
    return SiteContent().model_dump()

@app.get("/services")
def list_services():
    if db:
        items = get_documents("serviceitem", {})
        for it in items:
            it["_id"] = str(it.get("_id"))
        return items
    return []

@app.get("/portfolio")
def list_portfolio(category: Optional[str] = None):
    filt = {"category": category} if category else {}
    items = get_documents("portfolioitem", filt) if db else []
    for it in items:
        it["_id"] = str(it.get("_id"))
    return items

@app.get("/videos")
def list_videos():
    items = get_documents("videoitem", {}) if db else []
    for it in items:
        it["_id"] = str(it.get("_id"))
    return items

@app.get("/photos")
def list_photos():
    items = get_documents("photoitem", {}) if db else []
    for it in items:
        it["_id"] = str(it.get("_id"))
    return items

# ------------------------
# Admin endpoints (simple CMS)
# ------------------------
class UpdateContent(BaseModel):
    brand: Optional[str] = None
    colors: Optional[Dict[str, str]] = None
    hero_title: Optional[str] = None
    hero_cta: Optional[str] = None
    about_paragraphs: Optional[List[str]] = None

@app.post("/admin/content")
def update_content(payload: UpdateContent):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if db:
        create_document("sitecontent", data)
    return {"ok": True}

@app.post("/admin/services")
def add_service(item: ServiceItem):
    if db:
        _id = create_document("serviceitem", item)
        return {"ok": True, "id": _id}
    raise HTTPException(500, "Database not configured")

@app.post("/admin/portfolio")
def add_portfolio(item: PortfolioItem):
    if db:
        _id = create_document("portfolioitem", item)
        return {"ok": True, "id": _id}
    raise HTTPException(500, "Database not configured")

@app.post("/admin/video")
def add_video(item: VideoItem):
    if db:
        _id = create_document("videoitem", item)
        return {"ok": True, "id": _id}
    raise HTTPException(500, "Database not configured")

@app.post("/admin/photo")
def add_photo(item: PhotoItem):
    if db:
        _id = create_document("photoitem", item)
        return {"ok": True, "id": _id}
    raise HTTPException(500, "Database not configured")

@app.post("/contact")
def contact(msg: ContactMessage):
    if db:
        _id = create_document("contactmessage", msg)
        return {"ok": True, "id": _id}
    return {"ok": True}
