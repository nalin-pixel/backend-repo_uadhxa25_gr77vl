from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict

class SiteContent(BaseModel):
    brand: str = Field(default="VDRONE")
    colors: Dict[str, str] = Field(default_factory=lambda: {
        "primary": "#00C2FF",
        "bg": "#0A0F19",
        "text": "#FFFFFF",
        "black": "#000000"
    })
    hero_title: str = Field(default="VDRONE – Explore the world from above")
    hero_cta: str = Field(default="Explorează Portofoliul")
    about_paragraphs: List[str] = Field(default_factory=lambda: [
        "Filmări aeriene spectaculoase la rezoluții 4K/8K.",
        "Fotografie profesională pentru imobiliare, evenimente și branduri.",
        "Inspecții industriale, cartografiere și producție corporate."
    ])

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
