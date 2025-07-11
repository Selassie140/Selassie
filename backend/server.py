from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Birthday Club API", description="Customer Management System for Birthday Club")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.birthday_club

# Pydantic models
class CustomerSignup(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    date_of_birth: date
    customer_type: str  # "subscription", "non_subscription", "corporate"

class CustomerProfile(BaseModel):
    account_number: str
    contact_name: str
    email_address: EmailStr
    employment_title: Optional[str] = None
    phone_number: str
    birthday_date: date
    favorite_bistro_food_items: Optional[str] = None
    preferred_bistro_beverage: Optional[str] = None
    interest_in_group_private_package: Optional[str] = None
    music_ambiance_preference: Optional[str] = None
    allergies: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    celebration_budget: Optional[str] = None
    group_size_solo: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    want_corporate_offers: Optional[bool] = False
    preferred_celebration_style: Optional[str] = None
    personalized_bistro_birthday_treats: Optional[str] = None
    interest_in_rewards: Optional[bool] = False
    i_like_surprises: Optional[bool] = False
    special_notes: Optional[str] = None

class CustomerResponse(BaseModel):
    id: str
    account_number: str
    customer_profile_number: Optional[str] = None
    customer_type: str
    name: str
    email: str
    phone_number: str
    date_of_birth: date
    profile_completed: bool
    created_at: datetime
    updated_at: datetime

# Helper functions
def generate_account_number(customer_type: str, count: int) -> str:
    """Generate account number based on customer type"""
    if customer_type == "subscription":
        return f"SAN-{count:05d}"
    elif customer_type == "non_subscription":
        return f"NSAN-{count:05d}"
    elif customer_type == "corporate":
        return f"CSAN-{count:05d}"
    else:
        return f"GEN-{count:05d}"

def generate_profile_number(customer_type: str, count: int) -> str:
    """Generate customer profile number based on customer type"""
    if customer_type == "subscription":
        return f"SCPN-{count:05d}"
    elif customer_type == "non_subscription":
        return f"NSCPN-{count:05d}"
    elif customer_type == "corporate":
        return f"CSCPN-{count:05d}"
    else:
        return f"GCPN-{count:05d}"

async def get_next_account_number(customer_type: str) -> str:
    """Get the next available account number for customer type"""
    collection = db.customers
    
    # Count existing customers of this type
    count = await collection.count_documents({"customer_type": customer_type})
    return generate_account_number(customer_type, count + 1)

async def get_next_profile_number(customer_type: str) -> str:
    """Get the next available profile number for customer type"""
    collection = db.customers
    
    # Count existing customers of this type with completed profiles
    count = await collection.count_documents({
        "customer_type": customer_type,
        "profile_completed": True
    })
    return generate_profile_number(customer_type, count + 1)

# API Routes
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "birthday-club-api"}

@app.post("/api/customers/signup", response_model=CustomerResponse)
async def customer_signup(customer: CustomerSignup):
    """Initial customer signup with 4 basic fields"""
    try:
        # Generate account number
        account_number = await get_next_account_number(customer.customer_type)
        
        # Create customer document
        customer_doc = {
            "id": str(uuid.uuid4()),
            "account_number": account_number,
            "customer_profile_number": None,
            "customer_type": customer.customer_type,
            "name": customer.name,
            "email": customer.email,
            "phone_number": customer.phone_number,
            "date_of_birth": customer.date_of_birth,
            "profile_completed": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into database
        result = await db.customers.insert_one(customer_doc)
        
        if result.inserted_id:
            return CustomerResponse(**customer_doc)
        else:
            raise HTTPException(status_code=500, detail="Failed to create customer")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/customers/{account_number}/profile")
async def complete_customer_profile(account_number: str, profile: CustomerProfile):
    """Complete detailed customer profile with 20 fields"""
    try:
        # Find customer by account number
        customer = await db.customers.find_one({"account_number": account_number})
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Generate profile number if not already completed
        if not customer.get("profile_completed"):
            profile_number = await get_next_profile_number(customer["customer_type"])
        else:
            profile_number = customer.get("customer_profile_number")
        
        # Update customer with profile information
        profile_data = profile.dict()
        profile_data["customer_profile_number"] = profile_number
        profile_data["profile_completed"] = True
        profile_data["updated_at"] = datetime.utcnow()
        
        # Update database
        result = await db.customers.update_one(
            {"account_number": account_number},
            {"$set": profile_data}
        )
        
        if result.modified_count:
            # Return updated customer
            updated_customer = await db.customers.find_one({"account_number": account_number})
            return CustomerResponse(**updated_customer)
        else:
            raise HTTPException(status_code=500, detail="Failed to update customer profile")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers", response_model=List[CustomerResponse])
async def get_customers(
    customer_type: Optional[str] = None,
    profile_completed: Optional[bool] = None,
    limit: int = 50,
    skip: int = 0
):
    """Get customers with optional filtering"""
    try:
        # Build query filters
        query = {}
        if customer_type:
            query["customer_type"] = customer_type
        if profile_completed is not None:
            query["profile_completed"] = profile_completed
        
        # Execute query
        cursor = db.customers.find(query).skip(skip).limit(limit).sort("created_at", -1)
        customers = await cursor.to_list(length=limit)
        
        return [CustomerResponse(**customer) for customer in customers]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/{account_number}", response_model=CustomerResponse)
async def get_customer(account_number: str):
    """Get specific customer by account number"""
    try:
        customer = await db.customers.find_one({"account_number": account_number})
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return CustomerResponse(**customer)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/{account_number}/profile")
async def get_customer_profile(account_number: str):
    """Get detailed customer profile"""
    try:
        customer = await db.customers.find_one({"account_number": account_number})
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        if not customer.get("profile_completed"):
            raise HTTPException(status_code=404, detail="Customer profile not completed")
        
        return customer
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get customer statistics"""
    try:
        total_customers = await db.customers.count_documents({})
        subscription_customers = await db.customers.count_documents({"customer_type": "subscription"})
        non_subscription_customers = await db.customers.count_documents({"customer_type": "non_subscription"})
        corporate_customers = await db.customers.count_documents({"customer_type": "corporate"})
        completed_profiles = await db.customers.count_documents({"profile_completed": True})
        
        return {
            "total_customers": total_customers,
            "subscription_customers": subscription_customers,
            "non_subscription_customers": non_subscription_customers,
            "corporate_customers": corporate_customers,
            "completed_profiles": completed_profiles,
            "profile_completion_rate": (completed_profiles / total_customers * 100) if total_customers > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)