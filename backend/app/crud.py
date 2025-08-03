from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, extract
from typing import List, Optional
from datetime import datetime, date, timedelta
from app import models, schemas

# Resident CRUD operations
def get_resident(db: Session, resident_id: int):
    return db.query(models.Resident).filter(models.Resident.id == resident_id).first()

def get_residents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resident).offset(skip).limit(limit).all()

def get_recent_residents(db: Session, limit: int = 10):
    return db.query(models.Resident).order_by(models.Resident.created_at.desc()).limit(limit).all()

def create_resident(db: Session, resident: schemas.ResidentCreate):
    db_resident = models.Resident(**resident.dict())
    db.add(db_resident)
    db.commit()
    db.refresh(db_resident)
    return db_resident

def update_resident(db: Session, resident_id: int, resident: schemas.ResidentUpdate):
    db_resident = db.query(models.Resident).filter(models.Resident.id == resident_id).first()
    if db_resident:
        update_data = resident.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_resident, field, value)
        db.commit()
        db.refresh(db_resident)
    return db_resident

def delete_resident(db: Session, resident_id: int):
    db_resident = db.query(models.Resident).filter(models.Resident.id == resident_id).first()
    if db_resident:
        db.delete(db_resident)
        db.commit()
        return True
    return False

def search_residents(db: Session, query: str):
    return db.query(models.Resident).filter(
        or_(
            models.Resident.name.contains(query),
            models.Resident.room_number.contains(query),
            models.Resident.phone.contains(query)
        )
    ).all()

# Dashboard statistics
def get_total_residents_count(db: Session):
    return db.query(models.Resident).filter(models.Resident.status == models.ResidentStatus.ACTIVE).count()

def get_residents_under_medication_count(db: Session):
    return db.query(models.Resident).join(models.Medication).filter(
        and_(
            models.Resident.status == models.ResidentStatus.ACTIVE,
            models.Medication.is_active == True
        )
    ).distinct().count()

def get_vacant_beds_count(db: Session):
    return db.query(models.Bed).filter(models.Bed.status == models.BedStatus.VACANT).count()

def get_upcoming_birthdays_count(db: Session, days: int = 7):
    today = date.today()
    upcoming_date = today + timedelta(days=days)
    
    # Handle year boundary crossing
    if today.year == upcoming_date.year:
        return db.query(models.Resident).filter(
            and_(
                models.Resident.status == models.ResidentStatus.ACTIVE,
                extract('month', models.Resident.date_of_birth) >= today.month,
                extract('month', models.Resident.date_of_birth) <= upcoming_date.month,
                or_(
                    extract('month', models.Resident.date_of_birth) > today.month,
                    and_(
                        extract('month', models.Resident.date_of_birth) == today.month,
                        extract('day', models.Resident.date_of_birth) >= today.day
                    )
                ),
                or_(
                    extract('month', models.Resident.date_of_birth) < upcoming_date.month,
                    and_(
                        extract('month', models.Resident.date_of_birth) == upcoming_date.month,
                        extract('day', models.Resident.date_of_birth) <= upcoming_date.day
                    )
                )
            )
        ).count()
    else:
        return db.query(models.Resident).filter(
            and_(
                models.Resident.status == models.ResidentStatus.ACTIVE,
                or_(
                    and_(
                        extract('month', models.Resident.date_of_birth) >= today.month,
                        or_(
                            extract('month', models.Resident.date_of_birth) > today.month,
                            and_(
                                extract('month', models.Resident.date_of_birth) == today.month,
                                extract('day', models.Resident.date_of_birth) >= today.day
                            )
                        )
                    ),
                    and_(
                        extract('month', models.Resident.date_of_birth) <= upcoming_date.month,
                        or_(
                            extract('month', models.Resident.date_of_birth) < upcoming_date.month,
                            and_(
                                extract('month', models.Resident.date_of_birth) == upcoming_date.month,
                                extract('day', models.Resident.date_of_birth) <= upcoming_date.day
                            )
                        )
                    )
                )
            )
        ).count()

# Birthday operations
def get_upcoming_birthdays(db: Session, days: int = 7):
    today = date.today()
    residents = db.query(models.Resident).filter(models.Resident.status == models.ResidentStatus.ACTIVE).all()
    
    upcoming_birthdays = []
    for resident in residents:
        # Calculate next birthday
        this_year_birthday = resident.date_of_birth.replace(year=today.year)
        if this_year_birthday < today:
            next_birthday = resident.date_of_birth.replace(year=today.year + 1)
        else:
            next_birthday = this_year_birthday
        
        days_until = (next_birthday - today).days
        if 0 <= days_until <= days:
            birthday_info = schemas.ResidentBirthday(
                id=resident.id,
                name=resident.name,
                date_of_birth=resident.date_of_birth,
                age=resident.age,
                room_number=resident.room_number,
                days_until_birthday=days_until
            )
            upcoming_birthdays.append(birthday_info)
    
    return sorted(upcoming_birthdays, key=lambda x: x.days_until_birthday)

def get_today_birthdays(db: Session):
    today = date.today()
    residents = db.query(models.Resident).filter(
        and_(
            models.Resident.status == models.ResidentStatus.ACTIVE,
            extract('month', models.Resident.date_of_birth) == today.month,
            extract('day', models.Resident.date_of_birth) == today.day
        )
    ).all()
    
    return [
        schemas.ResidentBirthday(
            id=resident.id,
            name=resident.name,
            date_of_birth=resident.date_of_birth,
            age=resident.age,
            room_number=resident.room_number,
            days_until_birthday=0
        )
        for resident in residents
    ]

# Medication CRUD operations
def create_medication(db: Session, medication: schemas.MedicationCreate):
    db_medication = models.Medication(**medication.dict())
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

def get_resident_medications(db: Session, resident_id: int):
    return db.query(models.Medication).filter(
        and_(
            models.Medication.resident_id == resident_id,
            models.Medication.is_active == True
        )
    ).all()

# Checkup CRUD operations
def create_checkup(db: Session, checkup: schemas.CheckupCreate):
    db_checkup = models.Checkup(**checkup.dict())
    db.add(db_checkup)
    db.commit()
    db.refresh(db_checkup)
    return db_checkup

def get_checkups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Checkup).offset(skip).limit(limit).all()

def get_today_checkups(db: Session):
    today = date.today()
    return db.query(models.Checkup).filter(
        and_(
            func.date(models.Checkup.scheduled_date) == today,
            models.Checkup.status == models.CheckupStatus.SCHEDULED
        )
    ).all()

def get_resident_checkups(db: Session, resident_id: int):
    return db.query(models.Checkup).filter(models.Checkup.resident_id == resident_id).all()

# Event CRUD operations
def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def get_upcoming_events(db: Session, days: int = 7):
    today = datetime.now()
    upcoming_date = today + timedelta(days=days)
    return db.query(models.Event).filter(
        and_(
            models.Event.event_date >= today,
            models.Event.event_date <= upcoming_date,
            models.Event.status.in_([models.EventStatus.PLANNED, models.EventStatus.ONGOING])
        )
    ).order_by(models.Event.event_date).all()

# Document CRUD operations
def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(
        **document.dict(),
        original_filename=document.filename
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()

def get_resident_documents(db: Session, resident_id: int):
    return db.query(models.Document).filter(models.Document.resident_id == resident_id).all()

# Bed CRUD operations
def create_bed(db: Session, bed: schemas.BedCreate):
    db_bed = models.Bed(**bed.dict())
    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)
    return db_bed

def get_beds(db: Session):
    return db.query(models.Bed).all()

def get_vacant_beds(db: Session):
    return db.query(models.Bed).filter(models.Bed.status == models.BedStatus.VACANT).all()

def assign_bed_to_resident(db: Session, bed_id: int, resident_id: int):
    # Check if bed is vacant
    bed = db.query(models.Bed).filter(models.Bed.id == bed_id).first()
    if not bed or bed.status != models.BedStatus.VACANT:
        return False
    
    # Check if resident exists and doesn't already have a bed
    resident = db.query(models.Resident).filter(models.Resident.id == resident_id).first()
    if not resident:
        return False
    
    # Assign bed
    bed.status = models.BedStatus.OCCUPIED
    resident.bed_id = bed_id
    resident.room_number = bed.room_number
    
    db.commit()
    return True

def release_bed(db: Session, bed_id: int):
    bed = db.query(models.Bed).filter(models.Bed.id == bed_id).first()
    if not bed:
        return False
    
    # Find resident using this bed and remove assignment
    resident = db.query(models.Resident).filter(models.Resident.bed_id == bed_id).first()
    if resident:
        resident.bed_id = None
    
    bed.status = models.BedStatus.VACANT
    db.commit()
    return True

# Staff CRUD operations
def create_staff(db: Session, staff: schemas.StaffCreate):
    db_staff = models.Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def get_staff(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Staff).filter(models.Staff.is_active == True).offset(skip).limit(limit).all()

# Visitor CRUD operations
def create_visitor(db: Session, visitor: schemas.VisitorCreate):
    db_visitor = models.Visitor(**visitor.dict())
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor

def get_visitors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visitor).offset(skip).limit(limit).all()

def get_resident_visitors(db: Session, resident_id: int):
    return db.query(models.Visitor).filter(models.Visitor.resident_id == resident_id).all()

# Billing CRUD operations
def create_billing(db: Session, billing: schemas.BillingCreate):
    db_billing = models.Billing(**billing.dict())
    db.add(db_billing)
    db.commit()
    db.refresh(db_billing)
    return db_billing

def get_billing(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Billing).offset(skip).limit(limit).all()

def get_resident_billing(db: Session, resident_id: int):
    return db.query(models.Billing).filter(models.Billing.resident_id == resident_id).all()
