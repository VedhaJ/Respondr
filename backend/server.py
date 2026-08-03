from fastapi import FastAPI, APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from dotenv import load_dotenv
from pathlib import Path
import os
# -------------------------
# APP INIT
# -------------------------
app = FastAPI(title="Respondr API")
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ENV + DB SETUP
# -------------------------

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "respondr_db")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

# -------------------------
# MODELS
# -------------------------

class Incident(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    platform: str
    category: str
    title: str
    description: str
    icon: str


class RecoveryLink(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    platform: str
    title: str
    url: str
    description: str
    verified: bool


class PreventionTip(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    platform: str
    tips: List[str]


class NavigationGuide(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    platform: str
    official_url: str
    steps: List[str]
    warning: str

# -------------------------
# DATABASE SEEDING
# -------------------------

async def init_db():

    # -------------------------
    # Incidents
    # -------------------------
    if await db.incidents.count_documents({}) == 0:
        await db.incidents.insert_many([
            {
                "platform": "Instagram",
                "category": "social_media",
                "title": "Instagram Account Hacked",
                "description": "Your account has been compromised",
                "icon": "Instagram",
            },
            {
                "platform": "Facebook",
                "category": "social_media",
                "title": "Facebook Account Hacked",
                "description": "Someone else is using your account",
                "icon": "Facebook",
            },
            {
                "platform": "Twitter",
                "category": "social_media",
                "title": "Twitter Account Hacked",
                "description": "Unauthorized login detected",
                "icon": "Twitter",
            },
            {
                "platform": "WhatsApp",
                "category": "messaging",
                "title": "WhatsApp Account Taken Over",
                "description": "Someone accessed your WhatsApp",
                "icon": "MessageCircle",
            },
            {
                "platform": "Outlook",
                "category": "email",
                "title": "Outlook Account Compromised",
                "description": "Suspicious activity detected",
                "icon": "Mail",
            },
            {
                "platform": "upi-bank-fraud",
                "category": "financial",
                "title": "UPI Bank Fraud",
                "description": "Unauthorized transaction or scam",
                "icon": "ShieldCheck",
            },
            {
                "platform": "TAFCOP Mobile Check",
                "category": "mobile_security",
                "title": "Check Linked Mobile Numbers (TAFCOP)",
                "description": "Verify SIM cards linked to your ID",
                "icon": "ShieldCheck",
            },
        ])

    # -------------------------
    # Prevention Tips 
    # -------------------------
    if await db.prevention_tips.count_documents({}) == 0:
        await db.prevention_tips.insert_many([
            {
                "platform": "Instagram",
                "tips": [
                    "Enable Two-Factor Authentication (2FA).",
                    "Do not click suspicious DM links.",
                    "Review login activity regularly.",
                    "Avoid sharing OTP codes."
                ]
            },
            {
                "platform": "Facebook",
                "tips": [
                    "Turn on Two-Factor Authentication.",
                    "Avoid accepting unknown friend requests.",
                    "Check active sessions regularly.",
                    "Do not click fake giveaway links."
                ]
            },
            {
                "platform": "Twitter",
                "tips": [
                    "Enable 2FA using authenticator app.",
                    "Avoid crypto giveaway scams.",
                    "Review third-party app access.",
                    "Do not trust suspicious DMs."
                ]
            },
            {
                "platform": "WhatsApp",
                "tips": [
                    "Enable Two-Step Verification PIN.",
                    "Never share your 6-digit code.",
                    "Lock WhatsApp with fingerprint.",
                    "Beware of fake job/investment scams."
                ]
            },
            {
                "platform": "Outlook",
                "tips": [
                    "Enable Microsoft Two-Step Verification.",
                    "Use strong, unique passwords.",
                    "Avoid suspicious attachments.",
                    "Enable login alerts."
                ]
            },
            {
                "platform": "upi-bank-fraud",
                "tips": [
                    "Never share your UPI PIN.",
                    "Do not approve unknown collect requests.",
                    "Verify merchant name before payment.",
                    "Call 1930 immediately if fraud occurs."
                ]
            },
            {
                "platform": "TAFCOP Mobile Check",
                "tips": [
                    "Check linked mobile numbers regularly.",
                    "Report unknown SIM cards immediately.",
                    "Do not share Aadhaar details unnecessarily.",
                    "Use only official government portal."
                ]
            }
        ])

    # -------------------------
    # Recovery Links
    # -------------------------
    if await db.recovery_links.count_documents({}) == 0:
        await db.recovery_links.insert_many([
            {
                "platform": "Instagram",
                "title": "Instagram Recovery",
                "url": "https://www.instagram.com/hacked/",
                "description": "Official Instagram recovery page",
                "verified": True
            },
            {
                "platform": "Facebook",
                "title": "Facebook Recovery",
                "url": "https://www.facebook.com/hacked",
                "description": "Official Facebook recovery page",
                "verified": True
            },
            {
                "platform": "upi-bank-fraud",
                "title": "National Cyber Crime Portal",
                "url": "https://cybercrime.gov.in",
                "description": "Report financial fraud online",
                "verified": True
            },
            {
                "platform": "Twitter",
                "title": "Twitter Recovery",
                "url": "https://twitter.com/account/blocked",
                "description": "Official Twitter recovery page",
                "verified": True
            },
            {
                "platform": "WhatsApp",
                "title": "WhatsApp Support",
                "url": "https://www.whatsapp.com/contact",
                "description": "Contact WhatsApp support for account issues",
                "verified": True    
            },
            {
                "platform": "Outlook",
                "title": "Microsoft Account Recovery",
                "url": "https://account.live.com/password/reset",
                "description": "Official Microsoft account recovery page",
                "verified": True
            },
            {
                "platform": "TAFCOP Mobile Check",
                "title": "TAFCOP Official Portal",
                "url": "https://tafcop.sancharsaathi.gov.in",
                "description": "Check mobile numbers linked to your Aadhaar",
                "verified": True
            }
        ])

    # -------------------------
    # Navigation Guides
    # -------------------------        
    if await db.navigation_guides.count_documents({}) == 0:
        await db.navigation_guides.insert_many([

        {
            "platform": "Instagram",
            "official_url": "https://www.instagram.com/accounts/password/reset/",
            "steps": [
                "Go to the Instagram login page",
                "Click 'Forgot Password?'",
                "Select 'Need more help?'",
                "Submit account recovery request",
                "Verify using registered email or phone"
            ],
            "warning": "Only use instagram.com. Do not click recovery links from unknown messages."
        },

        {
            "platform": "Facebook",
            "official_url": "https://www.facebook.com/hacked",
            "steps": [
                "Go to facebook.com/hacked",
                "Click 'My Account is Compromised'",
                "Enter your registered email or phone number",
                "Follow identity verification steps",
                "Reset your password and review recent activity"
            ],
            "warning": "Always check the URL carefully. Avoid recovery links sent via suspicious emails."
        },

        {
  "platform": "Outlook",
  "official_url": "https://account.live.com/password/reset",
  "steps": [
    "Go to Outlook login page",
    "Click 'Forgot Password?'",
    "Enter your email address",
    "Verify using security method",
    "Create a new strong password"
  ],
  "warning": "Ensure the URL starts with account.live.com."
},

        {
            "platform": "WhatsApp",
            "official_url": "https://www.whatsapp.com/contact",
            "steps": [
                "Open WhatsApp on your phone",
                "Enter your phone number",
                "Verify using OTP sent via SMS",
                "If locked out, contact support@whatsapp.com",
                "Enable Two-Step Verification after recovery"
            ],
            "warning": "Never share your OTP with anyone. WhatsApp will never ask for OTP via chat."
        },

        {
            "platform": "Twitter",
            "official_url": "https://help.twitter.com/en/safety-and-security",
            "steps": [
                "Go to Twitter login page",
                "Click 'Forgot Password?'",
                "Enter your email, phone, or username",
                "Verify using email or SMS",
                "Reset password and enable Two-Factor Authentication"
            ],
            "warning": "Only use help.twitter.com for official support."
        },

        {
            "platform": "upi-bank-fraud",
            "official_url": "https://cybercrime.gov.in",
            "steps": [
                "Immediately call 1930 (National Cyber Crime Helpline)",
                "Visit cybercrime.gov.in",
                "Click 'Report Other Cyber Crime' or 'Report Financial Fraud'",
                "Fill in transaction details carefully",
                "Submit complaint and note down complaint number"
            ],
            "warning": "Report within 2 hours for higher chances of fund recovery. Never share bank OTP or CVV."
        },
        
        {
            "platform": "TAFCOP Mobile Check",
            "official_url": "https://tafcop.sancharsaathi.gov.in",
            "steps": [
                "Visit tafcop.sancharsaathi.gov.in",
                "Enter your mobile number",
                "Verify using OTP",
                "View list of SIM cards linked to your ID",
                "Report unknown numbers immediately"
            ],
             "warning": "Use only official government website. Never share OTP with anyone."
    }

    ])

# -------------------------
# ROUTES
# -------------------------

@app.on_event("startup")
async def startup():
    await init_db()

@api_router.get("/incidents", response_model=List[Incident])
async def get_incidents():
    incidents = await db.incidents.find().to_list(100)
    return [
        {
            "id": str(item["_id"]),
            "platform": item["platform"],
            "category": item["category"],
            "title": item["title"],
            "description": item["description"],
            "icon": item["icon"],
        }
        for item in incidents
    ]

@api_router.get("/prevention-tips", response_model=List[PreventionTip])
async def get_prevention_tips(platform: Optional[str] = Query(None)):
    
    query = {}
    if platform:
        query["platform"] = platform

    items = await db.prevention_tips.find(query).to_list(100)

    return [
        {
            "id": str(item["_id"]),
            "platform": item["platform"],
            "tips": item["tips"]
        }
        for item in items
    ]

@api_router.get("/recovery-links/{platform}", response_model=List[RecoveryLink])
async def get_recovery_links(platform: str):
    links = await db.recovery_links.find({"platform": platform}).to_list(100)
    return [
        {
            "id": str(item["_id"]),
            "platform": item["platform"],
            "title": item["title"],
            "url": item["url"],
            "description": item["description"],
            "verified": item.get("verified", True),
        }
        for item in links
    ]

@api_router.get("/navigation-guide/{platform}", response_model=NavigationGuide)
async def get_navigation_guide(platform: str):
    guide = await db.navigation_guides.find_one({"platform": platform})

    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    return {
        "id": str(guide["_id"]),
        "platform": guide["platform"],
        "official_url": guide["official_url"],
        "steps": guide["steps"],
        "warning": guide["warning"]
    }
# -------------------------
# FINALIZE
# -------------------------

app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown():
    client.close()