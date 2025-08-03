from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime, date

from app.database import SessionLocal, engine
from app import models, schemas, crud
from app.auth import get_current_user

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Old Age Home Management API",
    description="API for managing old age home residents, staff, and operations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploaded documents
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dashboard endpoints
@app.get("/api/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total_residents = crud.get_total_residents_count(db)
    under_medication = crud.get_residents_under_medication_count(db)
    vacant_beds = crud.get_vacant_beds_count(db)
    upcoming_birthdays = crud.get_upcoming_birthdays_count(db)
    
    return schemas.DashboardStats(
        total_residents=total_residents,
        under_medication=under_medication,
        vacant_beds=vacant_beds,
        upcoming_birthdays=upcoming_birthdays
    )

# Resident endpoints
@app.post("/api/residents/", response_model=schemas.Resident)
def create_resident(resident: schemas.ResidentCreate, db: Session = Depends(get_db)):
    """Add a new resident"""
    return crud.create_resident(db=db, resident=resident)

@app.get("/api/residents/", response_model=List[schemas.Resident])
def get_residents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all residents"""
    return crud.get_residents(db, skip=skip, limit=limit)

@app.get("/api/residents/recent", response_model=List[schemas.Resident])
def get_recent_residents(limit: int = 10, db: Session = Depends(get_db)):
    """Get recently added residents"""
    return crud.get_recent_residents(db, limit=limit)

@app.get("/api/residents/search")
def search_residents(query: str, db: Session = Depends(get_db)):
    """Search residents by name, room, or other criteria"""
    return crud.search_residents(db, query=query)

@app.get("/api/residents/{resident_id}", response_model=schemas.Resident)
def get_resident(resident_id: int, db: Session = Depends(get_db)):
    """Get a specific resident"""
    resident = crud.get_resident(db, resident_id=resident_id)
    if resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")
    return resident

@app.put("/api/residents/{resident_id}", response_model=schemas.Resident)
def update_resident(resident_id: int, resident: schemas.ResidentUpdate, db: Session = Depends(get_db)):
    """Update a resident"""
    db_resident = crud.update_resident(db, resident_id=resident_id, resident=resident)
    if db_resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")
    return db_resident

@app.delete("/api/residents/{resident_id}")
def delete_resident(resident_id: int, db: Session = Depends(get_db)):
    """Delete a resident"""
    success = crud.delete_resident(db, resident_id=resident_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resident not found")
    return {"message": "Resident deleted successfully"}

# Medication endpoints
@app.post("/api/medications/", response_model=schemas.Medication)
def create_medication(medication: schemas.MedicationCreate, db: Session = Depends(get_db)):
    """Add medication for a resident"""
    return crud.create_medication(db=db, medication=medication)

@app.get("/api/medications/resident/{resident_id}", response_model=List[schemas.Medication])
def get_resident_medications(resident_id: int, db: Session = Depends(get_db)):
    """Get all medications for a specific resident"""
    return crud.get_resident_medications(db, resident_id=resident_id)

# Birthday endpoints
@app.get("/api/birthdays/upcoming", response_model=List[schemas.ResidentBirthday])
def get_upcoming_birthdays(days: int = 7, db: Session = Depends(get_db)):
    """Get residents with upcoming birthdays"""
    return crud.get_upcoming_birthdays(db, days=days)

@app.get("/api/birthdays/today", response_model=List[schemas.ResidentBirthday])
def get_today_birthdays(db: Session = Depends(get_db)):
    """Get residents with birthdays today"""
    return crud.get_today_birthdays(db)

# Checkup endpoints
@app.post("/api/checkups/", response_model=schemas.Checkup)
def schedule_checkup(checkup: schemas.CheckupCreate, db: Session = Depends(get_db)):
    """Schedule a medical checkup"""
    return crud.create_checkup(db=db, checkup=checkup)

@app.get("/api/checkups/", response_model=List[schemas.Checkup])
def get_checkups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all scheduled checkups"""
    return crud.get_checkups(db, skip=skip, limit=limit)

@app.get("/api/checkups/today", response_model=List[schemas.Checkup])
def get_today_checkups(db: Session = Depends(get_db)):
    """Get today's scheduled checkups"""
    return crud.get_today_checkups(db)

@app.get("/api/checkups/resident/{resident_id}", response_model=List[schemas.Checkup])
def get_resident_checkups(resident_id: int, db: Session = Depends(get_db)):
    """Get checkups for a specific resident"""
    return crud.get_resident_checkups(db, resident_id=resident_id)

# Event endpoints
@app.post("/api/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    return crud.create_event(db=db, event=event)

@app.get("/api/events/", response_model=List[schemas.Event])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all events"""
    return crud.get_events(db, skip=skip, limit=limit)

@app.get("/api/events/upcoming", response_model=List[schemas.Event])
def get_upcoming_events(days: int = 7, db: Session = Depends(get_db)):
    """Get upcoming events"""
    return crud.get_upcoming_events(db, days=days)

# Document endpoints
@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    resident_id: Optional[int] = None,
    document_type: str = "general",
    db: Session = Depends(get_db)
):
    """Upload a document"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Create upload directory if it doesn't exist
    upload_dir = f"uploads/{document_type}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Save document record to database
    document = schemas.DocumentCreate(
        filename=file.filename,
        file_path=file_path,
        document_type=document_type,
        resident_id=resident_id
    )
    
    db_document = crud.create_document(db=db, document=document)
    
    return {
        "message": "Document uploaded successfully",
        "document_id": db_document.id,
        "filename": filename,
        "file_path": file_path
    }

@app.get("/api/documents/", response_model=List[schemas.Document])
def get_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all documents"""
    return crud.get_documents(db, skip=skip, limit=limit)

@app.get("/api/documents/resident/{resident_id}", response_model=List[schemas.Document])
def get_resident_documents(resident_id: int, db: Session = Depends(get_db)):
    """Get documents for a specific resident"""
    return crud.get_resident_documents(db, resident_id=resident_id)

# Bed management endpoints
@app.get("/api/beds/", response_model=List[schemas.Bed])
def get_beds(db: Session = Depends(get_db)):
    """Get all beds"""
    return crud.get_beds(db)

@app.get("/api/beds/vacant", response_model=List[schemas.Bed])
def get_vacant_beds(db: Session = Depends(get_db)):
    """Get vacant beds"""
    return crud.get_vacant_beds(db)

@app.post("/api/beds/", response_model=schemas.Bed)
def create_bed(bed: schemas.BedCreate, db: Session = Depends(get_db)):
    """Add a new bed"""
    return crud.create_bed(db=db, bed=bed)

@app.put("/api/beds/{bed_id}/assign/{resident_id}")
def assign_bed(bed_id: int, resident_id: int, db: Session = Depends(get_db)):
    """Assign a bed to a resident"""
    success = crud.assign_bed_to_resident(db, bed_id=bed_id, resident_id=resident_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not assign bed")
    return {"message": "Bed assigned successfully"}

@app.put("/api/beds/{bed_id}/release")
def release_bed(bed_id: int, db: Session = Depends(get_db)):
    """Release a bed (make it vacant)"""
    success = crud.release_bed(db, bed_id=bed_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bed not found")
    return {"message": "Bed released successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
