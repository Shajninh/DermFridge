from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import requests, urllib.parse, os, datetime

app = FastAPI()

# ---------- Database ----------
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ---------- Google OAuth ----------
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/google/callback"

@app.get("/")
def home():
    return {"message": "Welcome to DermFridge Backend ✅"}

@app.get("/add")
def add_item(name: str):
    db = SessionLocal()
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return {"status": "added", "item": item.name}

@app.get("/items")
def list_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return [{"id": i.id, "name": i.name, "date_added": i.date_added} for i in items]

@app.get("/auth/google")
def auth_google():
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
    )
    return RedirectResponse(url=auth_url)

@app.get("/auth/google/callback")
def auth_google_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()

    # Fetch user info
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {token_json['access_token']}"}
    ).json()

    name = user_info.get("name", "User")
    # Redirect to frontend
    return RedirectResponse(url=f"http://localhost:3000/welcome.html?name={urllib.parse.quote(name)}")
